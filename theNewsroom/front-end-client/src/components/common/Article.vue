<template>
<v-dialog d-flex style="box-shadow: none" elevation="0" v-model="show" width="1000px" height="500px">
   <v-card>
        <v-card-title class="headline" v-text="current_article.title" />
        <v-divider />
        <div>
            <v-card-text class="text-justify " v-text="current_article.articlecontentByContentId.content.slice(0, 500)+' ...'" />
        </div>
        <v-divider />
        <v-card-actions>
            <v-row dense>
                <v-col md6>
                    <v-card-title>
                        <strong>Publication Date</strong>: {{current_article.publicationDate.slice(0,10)}}
                    </v-card-title>
                </v-col>
                <v-col md6>
                    <v-card-title>
                        <strong>Media Outlet</strong>: {{current_article.mediaoutletByMediaOutletId.name}}
                    </v-card-title>

                </v-col>
            </v-row>
        </v-card-actions>
        <v-divider />
        <v-card-actions>
            <v-row dense>
                <v-btn rounded depressed :href="current_article.webContentUrl" target="_blank">
                    View Source
                </v-btn>
                <v-spacer />
                <v-btn rounded depressed @click.stop="close">
                    Back
                </v-btn>
            </v-row>
        </v-card-actions>
    </v-card>
</v-dialog>
</template>

<script>
import {
    mapState,
} from 'vuex';

export default {
    props: {
        value: Boolean
    },
    computed: {
        ...mapState(['current_article']),
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
