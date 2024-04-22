<template>  
  <div id="nav">
    <v-container>

      <v-data-table :items="items">
        <template v-slot:header.id="{ column }">
          {{ column.title.toUpperCase() }}
        </template>
      </v-data-table>

    </v-container>
  </div>
</template>

<script>
export default {
  created() {
    this.getDriverSummary()
  },
  data: () => ({
    items: [],
  }),
  methods:{
    getDriverSummary(){
      var drivingSummaryAPI = process.env.VUE_APP_API_URL + "/getDriverSummary"        
      fetch(drivingSummaryAPI, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          name: this.userName,
        })
      })
      .then((response) => response.json())
      .then((data) => {
        this.items = data
      })
    }
  },
}
</script>