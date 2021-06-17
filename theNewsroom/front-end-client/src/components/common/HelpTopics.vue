<template>
<div>
    <v-dialog d-flex elevation="0" v-model="show" width="500">
        <template v-slot:activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on">
                <v-icon>mdi-help-circle-outline</v-icon>
            </v-btn>
        </template>
        <v-card>
            <v-card-title class="headline">
                Need Help?
            </v-card-title>
            <v-card-text class="flex-wrap text-justify justify-space-between">
                <p>The <b>Navigation Bar</b> at the top of the page can be used to access any part of the website.</p>
                <p><b>Filters</b> is a drop down menu that will allow you to adjust the shown topics.</p>
                <p><b>Search</b> will allow you to search for a specific topic, regardless of whether it appears in the table.</p>
                <p>Adjusting the <b>Time Period</b> will allow you adjust the timeframe for the topics on the page.</p>
                <p>The <b>Media Outlet</b> search bar can be used to filter by articles included in your topic analysis by the publishing media outlet.</p>
                <p><b>The Topics Table</b> displays the topics matching your filters; or by default the most popular topics. You can use the sort buttons at the top of each column to change the order of the rows according to number of articles and topic title. You can also set the number of rows you want displayed at once, using the filter below the table, and view the next or previous set of rows with the arrows at the bottom.</p>
            </v-card-text>
            <v-card-actions>
                <v-btn width=100% rounded depressed @click.stop="close">
                    Close
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</div>
</template>

<script>
export default {
    props: {
        value: Boolean
    },
    methods: {
        close() {
            this.show = false
        },
    },
    data: () => ({
        show: false,
    }),
}
</script>