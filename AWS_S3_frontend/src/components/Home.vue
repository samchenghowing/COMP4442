<template>
  <div>
    <h2 class="display-2 font-weight-bold mb-3">COMP4442 Project</h2>
    <h1>Driving behavior analysis with AWS</h1>
    <p>Here you can monitor driving behavior in easily.</p>
    <router-link to="/drivingSummary">Driving summary</router-link>
    <p></p>
    <router-link to="/speedMonitoring">Driving Speed monitoring</router-link>
  </div>
</template>

<script>
export default {
  name: "HomePage",
};

</script>
