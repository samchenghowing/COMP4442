<template>
  <div id="nav">
    <v-container>

      <!-- <v-row>
        <v-col>
          <v-timeline align="start" density="compact">
            <v-timeline-item
              v-for="message in messages"
              :key="message.time"
              :dot-color="message.color"
              size="x-small"
            >
              <div class="mb-4">
                <div class="font-weight-normal">
                  <strong>{{ message.name }}</strong> @{{ message.time }}
                </div>
                <div>{{ message.content }}</div>
              </div>
            </v-timeline-item>
          </v-timeline>
        </v-col>
      </v-row> -->
      
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

      <v-row class="text-center">
        <div class="text-center ma-2">
          <v-snackbar
            v-model="snackbar"
          >
            {{ text }}
          </v-snackbar>
        </div>
      </v-row>

    </v-container>
  </div>
</template>

<script>
import io from "socket.io-client";
import { VSparkline } from 'vuetify/labs/VSparkline'

export default {
  name: "SpeedMonitoring",
  components: {
    VSparkline,
  },
  data() {
    return {
      user: "",
      messages: [],

      snackbar: false,
      text: `Hello, I'm a snackbar`,


      bandwidth: [5, 2, 5, 9, 5, 10, 3, 5, 3, 7, 1, 8, 2, 9, 6],
      requests: [1, 3, 8, 2, 9, 5, 10, 3, 5, 3, 7, 6, 8, 2, 9, 6],
      cache: [9, 9, 9, 9, 8.9, 9, 9, 9, 9, 9],

      
      startTime: "2017-01-01 00:00:00",
      endTime: "0",


      chatRoom: 1,
      socket: io(process.env.VUE_APP_API_URL),
    };
  },
  created() {
    this.socket.on('message', (data) => {
      var message = data["msg"]["msg"]
      var obj = JSON.parse(message)
      this.messages.push(obj)
    })
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
    joinRoom(){
      var obj = JSON.parse(sessionStorage.user)
      var name = obj["User info"]["name"]
      var userID = obj["User info"]["id"]
      var pwHash = obj["User info"]["pwHash"]
      var currentDate = new Date()

      this.socket.emit('joined', {
        msg: JSON.stringify({ 
          room: this.chatRoom,
          userID: userID,
          name: name,
          pwHash: pwHash,
          content: "joined",
          time: currentDate,
        })
      })
    },
    getDriverSpeed(){
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
        this.items = data
      })
    }
  },
};
</script>
  
  <style>
.chat-header {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 5rem;
  background-color: #f2f2f2;
  border-bottom: 1px solid #e2e2e2;
}

.chat-messages {
  height: calc(100vh - 10rem);
  overflow-y: scroll;
  padding: 4px;
  margin-bottom: 1rem;
}

.message {
  margin-bottom: 1rem;
}

.message-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.message-author {
  font-weight: bold;
}

.message-timestamp {
  color: #666;
}

.message-text {
  white-space: pre-wrap;
}

.chat-input {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 20px;
  /* background-color: #f2f2f2;
  border-top: 1px solid #e2e2e2; */
}

.chat-input input {
  flex-grow: 1;
  margin-right: 1rem;
  margin-left: 8px;
  margin-bottom: 2px;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 0.25rem;
}

.chat-input button {
  padding: 20px;
  border: none;
  background-color: #333;
  color: white;
  border-radius: 0.25rem;
  cursor: pointer;
}
</style>
  