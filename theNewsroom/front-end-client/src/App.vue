<template>
<div id="app">
    <span class="bg"></span>

    <v-app id="inspire">
        <Header />
        <router-view></router-view>
        <Footer />
    </v-app>
</div>
</template>

<script>
import Header from "./components/common/Header";
import Footer from "./components/common/Footer";

export default {
    name: "App",

    components: {
        Header,
        Footer
    },
    data: () => ({
        
    })
};
</script>

<style>
.body {
    padding-top: 50px;
}
</style>
