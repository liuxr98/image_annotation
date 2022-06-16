import Vue from "vue"

const state = () => ({
    loggedUser: ''
})

// getters
const getters = {
}

// actions
const actions = {
    getLoggerUser({commit}){
        Vue.axios.get('/users/info').then((response)=>{
            commit('setLoggedUser', response.data)
        }).catch(() => {
            commit('setLoggedUser', '')
        })
    }
}

// mutations
const mutations = {
    setLoggedUser(state, username){
        state.loggedUser = username
    },
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}