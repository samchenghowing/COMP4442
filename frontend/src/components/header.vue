<template>
    <v-card>
    <v-layout>
        <v-app-bar
        color="primary"
        density="compact"
        >
            <v-app-bar-nav-icon v-on:click.stop="drawer = !drawer"></v-app-bar-nav-icon>
            <v-toolbar-title>Driving behavior</v-toolbar-title>
            <template v-slot:append>
                <v-btn icon="mdi-dots-vertical" v-on:click="showSetting"></v-btn>
            </template>
        </v-app-bar>

        <v-navigation-drawer
            v-model="drawer"
            :location="$vuetify.display.mobile ? 'bottom' : undefined"
            temporary
        >
            <v-list>
                <v-list-item prepend-icon="mdi-home" title="Home" v-on:click="$router.push('/')"></v-list-item>
                <v-list-item prepend-icon="mdi-form-select" title="Driving summary" v-on:click="$router.push('/drivingSummary')"></v-list-item>
                <v-list-item prepend-icon="mdi-vector-curve" title="Speed monitoring" v-on:click="$router.push('/speedMonitoring')"></v-list-item>
            </v-list>
        </v-navigation-drawer>
    </v-layout>
    
    <v-divider></v-divider>
    </v-card>
</template>

<script>
export default {
    data() {
        return {
            drawer: null,
        }
    },
}
</script>