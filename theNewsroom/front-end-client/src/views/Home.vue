<template>
<div class="home">
    <v-container fluid>
        <v-col>
            <v-list-item>
                <v-text-field @keyup.enter.native="searchTopic" dense rounded filled v-model="keyword" append-icon="mdi-magnify" label="Looking for a specific topic?" single-line hide-details />
                <Search v-model="search" />
            </v-list-item>
        </v-col>
        <v-row>
            <!-- Topic of the Day -->
            <v-col   cols="12" md='6'>
                <v-card  color='rgb(230, 235, 255)' class="flex-wrap text-justify justify-space-between" height="100%" width="100%" hover @click="open(totd)">
                    <v-card-title class="headline">Topic of the Day</v-card-title>
                    <v-spacer/>
                    <v-card-text class="text-center font-weight-bold" v-resize-text v-text='totd.topicname' />
                    <v-card-text class='text-center'> {{totd.numofarticles}} articles</v-card-text>
                </v-card>
                <Popup v-model="popup" />
            </v-col>

            <!-- Login/Register/Saved -->
            <v-col   cols="12" md='6'>
                <!-- Show login/register when user is not authenticated -->
                <v-card  color='rgb(230, 235, 255)' v-if="!$auth.loading && !$auth.isAuthenticated" class="flex-wrap text-justify justify-space-between" height="100%" width="100%" hover @click.stop="login">
                    <v-card-title class="headline" v-text="unauth.title" />
                    <v-card-text >{{unauth.text}}</v-card-text>
                    <v-card-text class='text-center'> <strong>{{unauth.second_text}}</strong></v-card-text>
                </v-card>

                <!-- show saved/logout when user is authenticated -->
                <v-card  color='rgb(230, 235, 255)' v-else class="flex-wrap text-justify justify-space-between" height="100%" hover :to='saved.route'>
                    <v-card-title class="headline" v-text="saved.title" />
                    <v-card-text v-text='saved.text' />
                    <v-card-text class='text-center'> <strong>{{saved.second_text}}</strong></v-card-text>
                </v-card>
            </v-col>

            <!-- Topics/Trends -->
            <v-col dark v-for="card in cards" :key="card.id"   cols="12" md='6'>
                <v-card  color='rgb(230, 235, 255)' class=" flex-wrap text-justify justify-space-between" rounded height="100%" width="100%" hover :to='card.route'>
                    <v-card-title class="headline" v-text="card.title" />
                    <v-card-text> {{card.text}} </v-card-text>
                    <v-card-text class='text-center'> <strong>{{card.second_text}}</strong> </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</div>
</template>

<script>
import Popup from "../components/common/Popup";
import Search from "../components/common/Search";

import CREATE_USER from '../graphql/createUser.gql'
import CHECK_USER from '../graphql/checkUser.gql'
import GET_TOP_TOPIC from '../graphql/GetTopTopic.gql'
import {
    mapMutations
} from 'vuex';

export default {
    name: "Home",
    components: {
        Popup,
        Search
    },

    data() {
        return {
            skipQuery: false,
            user_id: '',
            user: null,
            popup: false,
            keyword: '',
            search: false,
            absolute: true,
            opacity: 10,
            overlay: false,
            unauth: {
                id: 'unreg',
                title: 'Log in for additional features!',
                text: ' Register an account or log in to get access to additional features, such as selecting more topics on your Trends graph and saving topics for later!',
                second_text: 'Click to Register or Log In!',

                route: '/register'
            },
            saved: {

                id: 'saved',
                title: 'My Saved Trends',
                text: 'Click here to view your saved trends, and explore how your selected topics are behaving!',
                second_text: 'Click to view your Saved Trends!',

                route: '/saved'
            },
            cards: [{
                    id: 'topics',
                    title: 'What is Topics?',
                    text: 'Sometimes, you just need to see the big picture. On the Topics page, you can explore the most popular news topics however you want. Adjust the time period, and filter by media outlets, to view which topics are the most prominent in the media landscape.',
                    second_text: 'Click to go to Topics!',

                    route: '/topics'
                },
                {
                    id: 'trends',
                    title: 'What is Trends?',
                    text: 'Looking to see how news topics change in relation to each other? Head to the Trends page to view the popularity of selected topics over time on a line graph. You can register an account for additional features, such as saving Trends configurations for later and selecting additional topics.',
                    second_text: 'Click to go to Trends!',
                    route: '/trends'
                }
            ],
            totd: {
                id: null,
                topicname: null,
                numofarticles: null
            }
        }
    },

    apollo: {
        totd: {
            query: GET_TOP_TOPIC,
            variables() {
                return {
                    limit: 1,
                    // The $to and $from here are pre-set for submission
                    startDate: "2020-11-11",
                    endDate: "2020-11-11",
                    // // If the database has been updated for the current date, pass the current date as argument
                    // to: (new Date()).toISOString().slice(0, 10),
                    // from: (new Date()).toISOString().slice(0, 10),
                }
            },
            update(data) {
                return data.gettoptopic;
            }
        },
        user : {
            query: CHECK_USER,
            variables() {
                return {
                    userId: this.user_id
                }
            },
            update(data) {
                return data;
            },
            skip() {
                return this.skipQuery
            },
        }
    },

    methods: {
        ...mapMutations([
            'openTopic',
            'searchTopicKeyword'

        ]),
        async createUser() {
            var userId = this.$auth.user.sub
            this.user_id = userId

            this.$apollo.queries.user.skip = false
            await this.$apollo.queries.user.refetch()
            if (this.user.allUsers.nodes.length == 0) {
                this.$apollo.mutate({
                    mutation: CREATE_USER,
                    variables: {
                        userId
                    }
                })
                console.log("New User: ", userId)
            } else {
                console.log("Existing User: ", userId)
            }
            
        },
        async login() {
            await this.$auth.loginWithPopup();
            this.createUser();
        },
        logout() {
            this.$auth.logout({
                returnTo: window.location.origin
            });
        },
        open(topic) {
            this.popup = true
            this.openTopic({
                id: topic.id,
                name: topic.topicname
            })
        },
        searchTopic() {
            this.search = true
            this.searchTopicKeyword(this.keyword)
        },

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
}
</script>

<style>
.card-outter {
    position: relative;
    padding-bottom: 50px;
}
.card-actions {
    position: relative;

    bottom: 0;
}
</style>
