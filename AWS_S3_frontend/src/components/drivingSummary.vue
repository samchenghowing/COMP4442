<template>  
  <div class="text-center">

    <v-data-table :items="items">
      <template v-slot:header.id="{ column }">
        {{ column.title.toUpperCase() }}
      </template>
    </v-data-table>

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
export default {
  created() {
    this.getDriverSummary()
  },
  data: () => ({
    items: [],
    dialog: true,
  }),
  methods:{
    getDriverSummary(){
      var drivingSummaryAPI = process.env.VUE_APP_API_URL + "/getDriverSummary"           
      fetch(drivingSummaryAPI, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          // name: this.userName,
        })
      })
      .then((response) => response.json())
      .then((data) => {
        this.items = data
        this.dialog = false
      })
    }
  },
}
</script>