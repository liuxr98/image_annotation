import Vue from "vue";
// initial state
const state = () => ({
    labelGroups: [],
    labels: [], // 当前处于标签管理界面的标签组的所有标签
})

// getters
const getters = {
}

// actions
const actions = {
    getLabelGroups({commit}){
       Vue.axios.get('/labelgroups/').then(response=>{
           commit('setLabelGroups', response.data)
       })
    },

    addLabelGroup({dispatch}, form){
        Vue.axios.post('/labelgroups/', form).then(()=>{
            dispatch('getLabelGroups')
        })
    },

    deleteLabelGroup({dispatch}, labelGroupID){
        Vue.axios.delete(`/labelgroups/${labelGroupID}`).then(() =>{
            dispatch('getLabelGroups')
        })
    },

    /*
        @desc 根据标签组ID获取该标签组的所有标签
     */
    getLabelsByID({commit}, labelGroupID){
       Vue.axios.get(`/labelgroups/${labelGroupID}/labels`).then(response =>{
           commit('setLabels', response.data)
       })
    },

    addLabel({dispatch}, payload){
        Vue.axios.post(`/labelgroups/${payload.labelGroupID}/labels` , {
            ...payload.label
        }).then(() =>{
            dispatch('getLabelsByID', payload.labelGroupID)
        })
    },

    updateLabel({commit}, label){
        Vue.axios.put(`/labelgroups/labels/${label.id}`,{
            ...label
        }).then(()=>{
            commit('updateLabel', label)
        })
    },

    deleteLabel({commit}, labelID){
      Vue.axios.delete(`/labelgroups/labels/${labelID}`).then(()=>{
          commit('deleteLabel', labelID)
      })
    }
}

// mutations
const mutations = {
    setLabelGroups(state, labelGroups){
        state.labelGroups = labelGroups
    },

    setLabels(state, labels){
        state.labels = labels
    },

    updateLabel(state, newLabel){
        let updatedLabel = state.labels.find(label => label.id === newLabel.id)
        Object.assign(updatedLabel, newLabel)
    },

    deleteLabel(state, labelID){
        let deletedLabelIndex = state.labels.findIndex(label => label.id === labelID)
        state.labels.splice(deletedLabelIndex, 1)
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
