<template>
  <div id="displayGroup">

    <!-- <v-timeline side="end">
      <v-timeline-item
        v-for="item in items"
        :key="item.id"
        :dot-color="item.color"
        size="small"
      >
        <v-alert
          :color="item.color"
          :icon="item.icon"
          :value="true"
        >
          Lorem ipsum dolor sit amet, no nam oblique veritus. Commune scaevola imperdiet nec ut, sed euismod convenire principes at. Est et nobis iisque percipit, an vim zril disputando voluptatibus, vix an salutandi sententiae.
        </v-alert>
      </v-timeline-item>
    </v-timeline> -->

    <v-row dense>
      <v-col v-for="(card, i) in cards" :key="i" cols="12" md="4">
        <v-card elevation="4">
          <div class="pa-4">
            <div class="ps-4 text-caption text-medium-emphasis">{{ card.title }}</div>

            <v-card-title class="pt-0 mt-n1 d-flex align-center">
              <div class="me-2">{{ card.value }}</div>

              <v-chip
                :color="card.color"
                :prepend-icon="`mdi-arrow-${card.change.startsWith('-') ? 'down' : 'up'}`"
                class="pe-1"
                size="x-small"
                label
              >
                <template v-slot:prepend>
                  <v-icon size="10"></v-icon>
                </template>

                <span class="text-caption">{{ card.change }}</span>
              </v-chip>
            </v-card-title>
          </div>

          <v-sparkline
            :color="card.color"
            :gradient="[`${card.color}E6`, `${card.color}33`, `${card.color}00`]"
            :model-value="card.data"
            height="50"
            line-width="1"
            min="0"
            padding="0"
            fill
            smooth
          ></v-sparkline>
        </v-card>
      </v-col>
    </v-row>

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
  mounted() {
    // get update every 30 seconds
    this.timer = setInterval(() => {
      this.getDriverSpeed()
    }, 30000)
  },
  data() {
    return {
      timer: null,

      dialog: true,

      bandwidth: [5, 2, 5, 9, 5, 10, 3, 5, 3, 7, 1, 8, 2, 9, 6],
      requests: [1, 3, 8, 2, 9, 5, 10, 3, 5, 3, 7, 6, 8, 2, 9, 6],
      cache: [9, 9, 9, 9, 8.9, 9, 9, 9, 9, 9],

      startTime: '2017-01-01T08:00:10.000',
      endTime: '2017-01-01T08:01:30.000',

      items: [
        {
          id: 1,
          color: 'info',
          icon: 'mdi-information',
        },
        {
          id: 2,
          color: 'error',
          icon: 'mdi-alert-circle',
        },
      ],

    };
  },
  computed: {
    cards () {
      return [
        {
          title: 'Bandwidth Used',
          value: '1.01 TB',
          change: '-20.12%',
          color: '#da5656',
          data: this.bandwidth,
        },
        {
          title: 'Requests Served',
          value: '7.96 M',
          change: '-7.73%',
          color: '#da5656',
          data: this.requests,
        },
        {
          title: 'Cache Hit Rate',
          value: '95.69 %',
          change: '0.75%',
          color: '#2fc584',
          data: this.cache,
        },
      ]
    },
  },
  methods: {
    getDriverSpeed(){
      var drivingSummaryAPI = process.env.VUE_APP_API_URL + "/getDriverSpeed"        
      fetch(drivingSummaryAPI, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          startTime: '2017-01-01T08:00:10.000',
          endTime: '2017-01-01T08:01:30.000',
        })
      })
      .then((response) => response.json())
      .then((data) => {
        this.items = data
        console.log(data)
        this.dialog = false
      })
    }
  },
  beforeDestroy() {
    clearInterval(this.timer)
  }
};
</script>
