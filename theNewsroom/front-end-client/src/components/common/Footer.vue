<template>
<v-footer flat class="footer">
    <v-col class="text-center" cols="12">
        <v-card flat class="text-center">
            <v-divider />
            <v-card-text class="pt-0">Here at the Newsroom, we want to show you more than just the news. We want to look beyond, to see how the news is told, and how the world is kept informed. </v-card-text>
            <v-card-text class="pt-0">The team here are:</v-card-text>
            <v-card-text class="pt-0 grey--text">
                <strong>Liam Dale</strong> |
                <strong>James Tatham</strong> |
                <strong>Lance Young</strong> |
                <strong>Jonothan Chan</strong> |
                <strong>Ronan O'Hara</strong>
            </v-card-text>
            <v-divider />
            <div>For a list of attributions and credits, see <a href="http://localhost:3000/credits">here.</a></div>
            <v-divider />

            <v-card-text>
                {{ new Date().getFullYear() }} —
                <strong>The Newsroom</strong>
            </v-card-text>
        </v-card>
    </v-col>
</v-footer>
</template>

<script>
export default {
    name: "Header",
    data: () => ({})
};
</script>

<style scoped>
footer {
    position: relative;
    align-self: center;
    width: auto;
    height: auto;
}
</style>
