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
                <p><b>Filters</b> is a drop down menu that can be used to search for specific topics, or change the time period of your <i>Trends</i> graph.</p>
                <p><b>Selected Topics</b> provides a list of the topics being displayed on the graph. You can remove topics from the list with the remove button.</p>
                <p><b>Related Topics</b> provides a range of topics most related to your current selection. You can add topics to the list with the add button.</p>
                <p>You can view a <b>Topic</b> by selecting it from the any part of the page.</p>
                <p><b>Saved Trends</b> will allow you to revisist saved selections, whilst selecting the <b>Save</b> button will save your current selection for later. This is only avaoiable for registered users, so remember to log in!</p>
                <p>You can also <b>Clear</b> your selection at any time.
                </p>
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