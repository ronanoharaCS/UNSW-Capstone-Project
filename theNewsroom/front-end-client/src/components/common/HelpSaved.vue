<template>
<div class="text-center">
    <v-dialog v-model="show" width="500">
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
                <p>Select any <b>Saved Trend</b> to be redirected to the <i>Trends</i> page with those topics preselected for you.
                </p>
                <p>You can view a <b>Topic</b> by selecting it from the saved trend.</p>
                <p>If you would like to removed a saved trend, simply select the <b>Delete</b> button.</p>
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