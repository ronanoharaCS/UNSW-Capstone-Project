<template>
<v-dialog d-flex elevation="0" v-model="show" width="1000px" height="500px">
    <v-card class=" flex-wrap text-justify justify-space-between">
        <v-card-title class="headline font-weight-bold">Maximum Topics Reached </v-card-title>
        <v-divider />
        <v-card-title class="subheading">
            Whoops! Up to 5 topics may be selected at once. 
        </v-card-title>
        <v-card-title class="subheading"> 
                    You can edit your selection from the Trends page
        </v-card-title>        
        <v-divider />
        <v-card-actions>
            <v-spacer/>
            <v-btn rounded depressed @click.stop="close">
                Close
            </v-btn>
        </v-card-actions>
    </v-card>
</v-dialog>
</template>

<script>
export default {
    props: {
        value: Boolean
    },
    computed: {
        show: {
            get() {
                return this.value
            },
            set(value) {
                this.$emit('input', value)
            }
        }
    },
    methods: {
        close() {
            this.show = false
        },
    },
    data: () => ({
    }),
}
</script>



