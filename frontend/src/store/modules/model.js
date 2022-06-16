import Vue from "vue"

const state = () => ({
    models: []
})

// getters
const getters = {
}

// actions
const actions = {
    getModels({commit}){
        Vue.axios.get('/models/').then(response=>{
            commit('setModels', response.data)
        })
    },
    deleteModel({dispatch}, id){
        Vue.axios.delete(`/models/${id}`).then(()=>{
            dispatch('getModels')
        })
    },
    trainModel({dispatch}, id){
        Vue.axios.post(`/models/${id}/train`).then(()=>{
            dispatch('getModels')
        })
    },
    evaluateModel({dispatch}, id){
        Vue.axios.post(`/models/${id}/evaluate`).then(()=>{
            dispatch('getModels')
        })
    }

}

// mutations
const mutations = {
    setModels(state, models){
        state.models = models
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}