<template>
<div class="saved">
<template>

    <v-container fluid>
        <h2 class="subheading grey--text text-center" v-if="configs.length == 0">Looks like you haven't saved any Trends yet! You can save a selection of topics on the Trends page.</h2>
        <v-row v-else>
            <v-list two-line width=100% rounded>
                <v-list-item>
                    <HelpSaved />
                    <span> Need Help?</span>

                </v-list-item>
                <v-list-item  class="item" v-for="config in configs" :key="config.id" depressed hover @click.stop="viewTrends(config.topics)">

                    <v-col d-flex>
                        <v-list-item-title class="headline" v-text="config.title" />
                        <v-card-actions>
                            <v-row dense>
                                <!-- We would need ot make sure we limit the number of characters shown -->
                                <v-col v-for="topic in config.topics" :key="topic.id">
                                    <v-btn dark rounded width=100% depressed @click.stop="open(topic)" v-text='topic.name' />
                                </v-col>
                            </v-row>
                            <v-col class="edit" dense>
                                    <v-btn outlined text rounded width=100% depressed @click.stop="deleteTrend(config)">
                                        Delete
                                    </v-btn>
                            </v-col>
                        </v-card-actions>
                    </v-col>
                </v-list-item>
            </v-list>
        </v-row>
        <Popup v-model="popup" />
    </v-container>
</template>
</div>
</template>

<script>
import Popup from "../components/common/Popup";
import HelpSaved from "../components/common/HelpSaved";
import USER_CONFIGS from "../graphql/AllOfAUsersConfigurations.gql"
import DELETE_USER_CONFIG from "../graphql/deleteUserConfiguration.gql"
import DELETE_TOPIC_CONFIG from "../graphql/deleteTopicConfiguration.gql"


import {
    mapMutations,
    mapGetters
} from 'vuex';

export default {
    name: "Topics",
    components: {
        Popup,
        HelpSaved
    },
    data: () => ({
        trend: {
            title: '',
            topics: []
        },
        dialog: false,
        popup: false,
        userId: '',
        configs: [],
        skipQuery: false
    }),
    computed: {
        ...mapGetters(['numSelected', 'getSelected', 'getRelated']),

    },
    apollo: {
        configs: {
            query: USER_CONFIGS,
            variables() {
                return {
                    usrId: this.$auth.user.sub
                }
            },
            update(data) {
                return data.allUserconfigurations.nodes.map(a => ({
                    id: a.id,
                    title: a.configName,
                    topics: a.topicconfigurationsByUsrConfigId.nodes.map(b => ({
                        nodeId: b.id,
                        id: b.topicId,
                        name: b.topicName
                    }))
                }))
            },
            skip() {
                return this.skipQuery
            },
        }
    },
    methods: {
        ...mapMutations([
            'openTopic',
            'setSelected',
        ]),
        open(title) {
            this.popup = true
            this.openTopic(title)
        },
        viewTrends(selection) {
            console.log(selection)

            selection = selection.map(a => ({
                    id: a.id,
                    name: a.name
                }))

            this.setSelected(selection)
            this.$router.push({
                name: 'trends'
            })
        },
        async getConfigs() {
            this.$apollo.queries.configs.skip = false
            await this.$apollo.queries.configs.refetch()
        },
        async deleteTrend(selection) {
            console.log("Deleting saved congifuration...")
            await this.deleteTopicConfig(selection.topics)
            await this.deleteUserConfig(selection.id)
            console.log("Saved congifuration deleted")
        },
        async deleteTopicConfig(topics) {
            var i
            for (i = 0; i < topics.length; i++) {
                var id = topics[i].nodeId
                this.$apollo.mutate({
                    mutation: DELETE_TOPIC_CONFIG,
                    variables: {
                        id,
                    }
                })
            }
        },
        async deleteUserConfig(id) {
            this.$apollo.mutate({
                mutation: DELETE_USER_CONFIG,
                variables: {
                    id,
                },
                update: () => {
                    this.getConfigs()
                },
            })
        },
    },
    mounted: function() {
        this.getConfigs()
    },
}
</script>

<style scoped>
td {
    text-align: center !important;
}
.saved {
    padding-top: 20px
}
.edit {
    max-width: 150px;
}
.item {
    background: rgb(230, 235, 255);
}
.item:hover {
    background:rgb(222, 229, 255);
}
</style>