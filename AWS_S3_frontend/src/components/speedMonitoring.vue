<template>
  <div id="displayGroup">

    <h2> Speed monitoring for current period:</h2>
    <h1>{{startTime}} to {{endTime}}</h1>
    <h3>Next update will be in: {{ timerCount }} seconds</h3>
   
    <div class="text-center" >
      <v-dialog
        width="auto"
        scrollable
        v-model="alertDialog"
      >
      <v-card
        prepend-icon="mdi-alert"
        title="Speeding Alert for current period"
        >
          <v-divider class="mt-3"></v-divider>
          <v-card-text class="px-4" style="height: 300px;">
            <v-alert
              density="compact"
              title="Speeding drivers (scoll down for more)"
              type="warning"
            >
              <v-timeline align="start" density="compact">
                <v-timeline-item
                  v-for="overspeedDriver in overspeedDrivers"
                  :key="overspeedDriver.speed_time"
                  size="x-small"
                >
                  <div class="mb-4">
                    <div class="font-weight-normal">
                      <strong>{{ overspeedDriver.carPlateNumber }}</strong> @{{ overspeedDriver.speed_time }}
                    </div>
                    <div>Speed: {{ overspeedDriver.speed }} km/h</div>
                  </div>
                </v-timeline-item>
              </v-timeline>
            </v-alert>
          </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-btn
              text="Clear alerts"
              @click="clearAlerts"
            ></v-btn>
          </v-card-actions>
      </v-card>

      </v-dialog>
    </div>
    
    <div v-for="card in cards" :key="card.driverID">
      <v-card
        :title=card.driverID
        :subtitle=card.carPlateNumber
        class="mt-8 mx-auto overflow-visible"
        max-width="600"
      >
      <v-card-title>Latest Speed: {{card.data.at(-1)}} km/h</v-card-title>
        <v-sparkline
          :model-value="card.data"
          :gradient="['#f72047', '#ffd200', '#1feaea']"
          height="50"
          line-width="2"
          min="0"
          padding="0"
          smooth="16"
          auto-draw
        ></v-sparkline>
      </v-card>
    </div>

    <!-- show loading -->
    <v-dialog
      v-model="dialog"
      max-width="400"
      persistent
    >
      <v-list
        class="py-2"
        color="primary"
        elevation="12"
        rounded="lg"
      >
        <v-list-item
          prepend-icon="mdi-aws"
          title="Retriving data from Lambda function..."
        >
          <template v-slot:prepend>
            <div class="pe-4">
              <v-icon color="primary" size="x-large"></v-icon>
            </div>
          </template>

          <template v-slot:append>
            <v-progress-circular
              color="primary"
              indeterminate="disable-shrink"
              size="16"
              width="2"
            ></v-progress-circular>
          </template>
        </v-list-item>
      </v-list>
    </v-dialog>

  </div>
</template>

<script>
import { VSparkline } from 'vuetify/labs/VSparkline'

export default {
  components: {
    VSparkline,
  },
  created() {
    this.getDriverSpeed()
  },
  data() {
    return {
      timerCount: 0,
      dialog: false,
      alertDialog: false,
      cards: null,
      startTime: '2017-01-01T08:00:00.000Z',
      endTime: '2017-01-01T08:03:00.000Z',
      overspeedDrivers: [],
    };
  },
  watch: {
    timerCount: {
      handler(value) {
          if (value > 0) {
              setTimeout(() => {
                  this.timerCount--;
              }, 1000);
          }
          if (value == 0) {
            this.getDriverSpeed()
          }
      },
      immediate: true // This ensures the watcher is triggered upon creation
    }
  },
  methods: {
    getDriverSpeed(){
      this.dialog = true

      // convert from ISOString
      var startDate = new Date(this.startTime);
      var endDate = new Date(this.endTime);

      // add 30 sec
      startDate.setSeconds(startDate.getSeconds() + 30);
      endDate.setSeconds(endDate.getSeconds() + 30);

      // convert to ISOString
      this.startTime = startDate.toISOString();
      this.endTime = endDate.toISOString();

      var drivingSummaryAPI = process.env.VUE_APP_API_URL + "/getDriverSpeed"        
      fetch(drivingSummaryAPI, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          startTime: this.startTime,
          endTime: this.endTime,
        })
      })
      .then((response) => response.json())
      .then((data) => {
        var itemsArray = data.flatMap(item => item.Items);

        const result = itemsArray.reduce((acc, item) => {
          const driverID = item.driverID.S;
          const carPlateNumber = item.carPlateNumber.S;
          const speed_time = item.speed_time.S;
          const speed = parseInt(item.Speed.S, 10);
          const isOverspeed = item.isOverspeed ? parseInt(item.isOverspeed.S, 10) : 0;
          if(isOverspeed == 1) this.overspeedDrivers.push({ driverID, carPlateNumber, speed, speed_time });

          const existingDriver = acc.find(driver => driver.driverID === driverID);
          if (existingDriver) {
            existingDriver.data.push(speed);
            existingDriver.isOverspeed = isOverspeed;
            existingDriver.carPlateNumber = carPlateNumber;
          } else {
            acc.push({ driverID, carPlateNumber, data: [speed], isOverspeed});
          }
          return acc;
        }, []);

        if (this.overspeedDrivers.length) this.alertDialog = true;
        console.log(this.overspeedDrivers);

        this.timerCount = 30
        this.cards = result
        this.dialog = false
      })
    },
    clearAlerts(){
      this.alertDialog = false
      this.overspeedDrivers = []
    }
  },
  beforeDestroy() {
    clearInterval(this.timer)
  }
};
</script>
