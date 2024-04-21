<template>  
  <div id="nav">
    <v-container>
      <v-row class="text-center">
        <div class="text-center ma-2">
          <v-snackbar
            v-model="snackbar"
          >
            {{ text }}
          </v-snackbar>
        </div>
      </v-row>

      <v-data-table-virtual
        :headers="headers"
        :items="DS_table"
        height="400"
        item-value="name"
      ></v-data-table-virtual>

    </v-container>
  </div>
</template>

<script>
export default {
  computed: {
    DS_table () {
      return [...Array(10).keys()].map(i => {
        const driver = { ...this.drivers[i % this.drivers.length] }
        driver.name = `${driver.name} #${i}`
        return driver
      })
    },
  },
  created() {

  },
  data: () => ({
    snackbar: false,
    loading: false,
    text: `Hello, I'm a snackbar`,
    headers: [
      { title: 'Boat Type', align: 'start', key: 'name' },
      { title: 'Speed (knots)', align: 'end', key: 'speed' },
      { title: 'Length (m)', align: 'end', key: 'length' },
      { title: 'Price ($)', align: 'end', key: 'price' },
      { title: 'Year', align: 'end', key: 'year' },
    ],
    drivers: [
      {
        name: 'Speedster',
        speed: 35,
        length: 22,
        price: 300000,
        year: 2021,
      },
      {
        name: 'OceanMaster',
        speed: 25,
        length: 35,
        price: 500000,
        year: 2020,
      },
      {
        name: 'Voyager',
        speed: 20,
        length: 45,
        price: 700000,
        year: 2019,
      },
      {
        name: 'WaveRunner',
        speed: 40,
        length: 19,
        price: 250000,
        year: 2022,
      },
      {
        name: 'SeaBreeze',
        speed: 28,
        length: 31,
        price: 450000,
        year: 2018,
      },
      {
        name: 'HarborGuard',
        speed: 18,
        length: 50,
        price: 800000,
        year: 2017,
      },
      {
        name: 'SlickFin',
        speed: 33,
        length: 24,
        price: 350000,
        year: 2021,
      },
      {
        name: 'StormBreaker',
        speed: 22,
        length: 38,
        price: 600000,
        year: 2020,
      },
      {
        name: 'WindSail',
        speed: 15,
        length: 55,
        price: 900000,
        year: 2019,
      },
      {
        name: 'FastTide',
        speed: 37,
        length: 20,
        price: 280000,
        year: 2022,
      },
    ],

  }),
  methods:{
    drivingSummary(){
      var drivingSummaryAPI = process.env.VUE_APP_API_URL + "/drivingSummary"        
      fetch(drivingSummaryAPI, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          name: this.userName,
        })
      })
      .then((response) => response.json())
      .then((user) => {
        console.log(JSON.stringify(user))
        this.loading = false
        this.snackbar = true
        this.text = user.status
      })
    },
  },

}
</script>