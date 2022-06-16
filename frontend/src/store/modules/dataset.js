import Vue from "vue";
// initial state
const state = () => ({
    datasets: [],
})

// getters
const getters = {
}

// actions
const actions= {
    getDatasets({commit}){
        Vue.axios.get('/datasets/').then(response =>{
            console.log(response.data)
            commit('setDatasets', response.data)
        })
    },

    deleteDataset({dispatch}, id){
        Vue.axios.delete(`/datasets/${id}`).then(() =>{
            dispatch('getDatasets')
        })
    },

    addDataset({dispatch}, form){
        Vue.axios.post('/datasets/',form).then( ()=>{
            dispatch('getDatasets')
        })
    },
}

// mutations
const mutations = {
    setDatasets(state, datasets){
        state.datasets = datasets
    },

    deleteDataset(state, id){
        let deletedDatasetIndex = state.datasets.findIndex(dataset => dataset.id === id)
        state.datasets.splice(deletedDatasetIndex, 1)
    },
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}