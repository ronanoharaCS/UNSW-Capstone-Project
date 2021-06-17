import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

// const URI = whatever we use for db

export default new Vuex.Store({
	
	state: {
		keyword: '',
		current_topic: {
			id: null,
			name: null
		},
		current_article: {
			id: null,
			title: null,
			publicationDate: '',
			webContentUrl: null,
			author: null,
			mediaoutletByMediaOutletId: {
				name: null,
			},
			articlecontentByContentId: {
				id: null,
				content: '',
			},
		},
		popups: [],
		selected: [],
		related: []
	},

	mutations: {
		addSelected(state, topic) {
			let index = state.selected.findIndex(item => item.id == topic.id)
			if (index == -1 && state.selected.length < 5){
				state.selected.push({
					id: topic.id,
					name: topic.name
				})
			}
		},
		removeSelected(state, topic) {
			let index = state.selected.findIndex(item => item == topic)
			state.selected.splice(index, 1)
		},
		openTopic(state, topic) {
			state.current_topic = topic
		},
		nextTopic(state, topic) {
			state.popups.push(state.current_topic)
			state.current_topic = topic
		},
		previousTopic(state) {
			state.current_topic = state.popups.pop()
		},
		closeTopic(state) {
			state.current_topic = ''
			state.popups = []
		},
		emptySelected(state) {
			state.selected = []
		},
		setSelected(state, selection) {
			state.selected = selection.map(a => a)
		},
		openArticle(state, article) {
			state.current_article = article.articleByArticleId
		},
		searchTopicKeyword(state, keyword) {
			state.keyword = keyword
		}
	},

	actions: {
		// fetchTopics() ---> to retrieve all topics in db
	},
	
	getters: {
		isRoot: state => {
			if (state.popups.length === 0) return true
			return false
		},
		numSelected: state => {
			return state.selected.length
		},
		isSelected: state => {
			let index = state.selected.findIndex(item => item.id == state.current_topic.id)
			if (index == -1) return false
			return true
		},
		getSelected: state => {
			return state.selected
		},
		getRelated: state => {
			// This will return the related topics based on the current topic (for popups) or selected topics (for trends)
			return state.related
		},
		getPopups: state => {
			return state.popups
		},
		getArticle: state => {
			return state.current_article
		},
		maxSelected: state => {
			if (state.selected.length < 5) return false
			return true
		}
	},
})



