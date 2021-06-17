<template>
<v-dialog v-model="save" max-width="600px" max-height="100px">
    <template v-slot:activator="{ on, attrs }">
        <v-btn depressed rounded v-bind="attrs" v-on="on">
            Save
        </v-btn>
    </template>
    <v-card class="flex-wrap text-justify justify-space-between">
        <v-card-title>
            <span class="headline">Save Trend Selection</span>
        </v-card-title>
        <v-card-text>
            <v-text-field v-model='title' :rules="[
                () => !!title || 'This field is required',
                () => !!title && this.getSelected.length > 0 || 'Please select a topic first', 
                () => !!title && title.length > 3 || 'Name must have more than 3 characters',
                () => !!title && title.length <= 25 || 'Name must be less than 20 characters', 
                ]" placeholder="Enter a name for your selection" counter="20" />
        </v-card-text>
        <v-card-actions>
            <v-spacer />
            <v-btn depressed rounded @click.stop="close">
                Close
            </v-btn>
            <v-btn depressed rounded @click="saveTrendSelection(title)">
                Save
            </v-btn>
        </v-card-actions>
    </v-card>
</v-dialog>
</template>

<script>
import {
    mapGetters,
    mapMutations
} from 'vuex';

import CREATE_USER_CONFIG from '../../graphql/createUserConfiguration.gql'
import CREATE_TOPIC_CONFIG from '../../graphql/createTopicConfiguration.gql'

export default {
    props: {
        value: Boolean
    },
    data: () => ({
        title: null,
        save: false,
        config_id: null
    }),
    computed: {
        ...mapGetters(['getSelected']),
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
        ...mapMutations([
            'saveTrend'
        ]),
        close() {
            this.save = false
            this.$emit('saved');
        },
        async saveTrendSelection(configName) {
            if (configName.length > 3 && configName.length <= 20 && this.getSelected.length > 0) {
                configName = configName.charAt(0).toUpperCase() + configName.slice(1)
                await this.createUserConfig(configName)
                this.close()
            }
        },
        async createUserConfig(configName) {
            var usrId = this.$auth.user.sub
            await this.$apollo.mutate({
                mutation: CREATE_USER_CONFIG,
                variables: {
                    configName,
                    usrId
                },
                update: (store, { data: { createUserconfiguration } }) => {
                    this.createTopicConfig(createUserconfiguration.userconfiguration.id)
                },
            })
        },
        async createTopicConfig(usrConfigId) {
            var i
            for (i = 0; i < this.getSelected.length; i++) {
                var topicId = this.getSelected[i].id
                var topicName = this.getSelected[i].name
                await this.$apollo.mutate({
                mutation: CREATE_TOPIC_CONFIG,
                    variables: {
                        usrConfigId,
                        topicId,
                        topicName
                    }
                })
            }
            console.log('end create topic')
        }
    },
}
</script>
