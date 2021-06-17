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
                <p><b>Related Topics</b> allow you to view information for those topics most related to this one.</p>
                <p><b>Top Articles</b> alllow you to view news articles most related to this topic.</p>
                <p><b>Add to Trends</b> will select the current topic and add it to your selected topics, so that you can view more information on the <i>Trends</i> page.</p>
                <p><b>Remove from Trends</b> will remove the current topic and from your selected topics.</p>
                <p><b>Previous</b> will display the last topic you were viewing. Selecting topics from <i>Related Topics</i> will keep a log of which topics you have visited, so you can always return.</p>
                <p><b>Close</b> will close this popup. Clicking anywhere other than this popup will also close it.</p>
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