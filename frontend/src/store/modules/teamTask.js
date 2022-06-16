import Vue from "vue";
const state = () => ({
    teamTasks: [],
    subtasks: [],
    teamTaskID: ''
})
// getters
const getters = {

}


// actions
const actions= {
    addTeamTask({dispatch}, teamtask){
        Vue.axios.post(`/teamtasks/`, teamtask).then(()=>{
            dispatch("getTeamTasks")
            dispatch('getSubTasks')
        })
    },

    getTeamTasks({commit}){
        Vue.axios.get(`/teamtasks/`).then(response =>{
            commit('setTeamTasks', response.data)
        })
    },

    deleteTeamTask({dispatch}, id){
        Vue.axios.delete(`/teamtasks/${id}`).then(()=>{
            dispatch('getTeamTasks')
            dispatch('getSubTasks')
        })
    },

    /*
        @desc 终止任务
        @param [Object] payload
            example:{
                        id: xxx_id # team_task id
                        reserved: [Boolean] # decide whether to reserve the annotations of submitted subtasks
                    }
     */
    terminateTeamTask({dispatch}, payload){
        Vue.axios.put(`/teamtasks/${payload.id}`, {
            actionType: 'Terminate',
            reserved: payload.reserved
        }).then(()=>{
            dispatch('getTeamTasks')
            dispatch('getSubTasks')
        })

    },
    reviewTeamTask({dispatch}, id){
        Vue.axios.put(`/teamtasks/${id}`, {
            actionType: 'Review',
        }).then(()=>{
            dispatch('getTeamTasks')
            dispatch('getSubTasks')
        })
    },
    getSubTasks({commit}){
        Vue.axios.get('/teamtasks/subs').then(response =>{
            commit('setSubTasks', response.data)
        })
    },

    submitSubtask({dispatch}, id){
        Vue.axios.put(`/teamtasks/subs/${id}`).then(() => {
            dispatch('getSubTasks')
        })
    }
}

// mutations
const mutations = {
    setTeamTasks(state, teamTasks){
        state.teamTasks = teamTasks
    },
    setSubTasks(state, subtasks){
        state.subtasks = subtasks
    },
    setTeamTaskID(state, id) {
        state.teamTaskID = id
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
