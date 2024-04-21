<template>
    <v-card>
    <v-layout>
        <v-app-bar
        color="primary"
        density="compact"
        >
        <v-app-bar-nav-icon v-on:click.stop="drawer = !drawer"></v-app-bar-nav-icon>

        <v-app-bar-title>Driving behavior</v-app-bar-title>

        <template v-slot:append>
            <v-btn icon="mdi-dots-vertical" v-on:click="showSetting"></v-btn>
        </template>
        </v-app-bar>

        <v-navigation-drawer
            v-model="drawer"
            temporary
        >
            <v-list density="compact" nav>
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
    mounted(){
        window.addEventListener('isAuth-changed', (event) => {
            this.isLoggedIn = event.detail.isAuth;
            var obj = JSON.parse(sessionStorage.user)
            this.UserName = obj["User info"]["name"]
        });
    },
    data() {
        return {
            isLoggedIn: false,
            drawer: null,
            dialog: false,
            UserName: "Guest user",
        }
    },
    methods:{
        logout(){
            sessionStorage.clear()
            this.isLoggedIn = false
            this.UserName = "Guest user"
            this.$router.push('/login')
        }
    },
}
</script>