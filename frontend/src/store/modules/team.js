import Vue from "vue";
// initial state
// const ApiState = {
//     INIT: 0,
//     LOADING: 1,
//     ERROR: 2,
//     LOADED: 3
// }
const state = () => ({
    teams: [],
    activeIndex: 0,
    activeTeamInfo: Object.create(null),
})

// getters
const getters = {
    teamsLength: (state) =>{
        return state.teams.length
    },
    activeTeamID: (state, getters)=>{
        if(getters.teamsLength === 0){
            return ""
        }
        return state.teams[state.activeIndex].id
    }
}


// actions
const actions= {
    getTeams({commit}){
        return new Promise((resolve)=>{
            Vue.axios.get('/teams/').then(response => {
                commit("setTeams", response.data)
                resolve()
            })
        })

    },

    deleteTeam({dispatch, getters, commit}){
        Vue.axios.delete(`/teams/${getters.activeTeamID}`).then(() =>{
            dispatch('getTeams').then(()=>{
                if(getters.teamsLength !== 0){
                    commit('setActiveIndex', 0) // 删除当前团队后，默认为列表的第一个团队
                }
            })
        })
    },

    addTeam({dispatch, getters, commit}, form){
      Vue.axios.post(`/teams/`, form).then(() =>{
          dispatch('getTeams').then(()=>{
              if(getters.teamsLength === 1){ // 意味着团队列表之前为空白，所以添加后自动显示第一个团队
                  commit('setActiveIndex', 0)
              }
          })
      })
    },

    deleteMember({dispatch},id) {
      Vue.axios.delete(`/teams/members/${id}`).then(()=>{
          dispatch('getTeamInfo')
          dispatch('getTeams')
      })
    },

    addMember({dispatch, getters}, member){
        Vue.axios.post(`/teams/${getters.activeTeamID}/members`, member).then((response)=>{
            console.log(response)
            dispatch(`getTeamInfo`)
            dispatch(`getTeams`)
        })
    },

    getTeamInfo({commit, getters}){
        if(getters.activeTeamID){
            Vue.axios.get(`/teams/${getters.activeTeamID}`).then(response =>{
                commit('setActiveMemberInfo', response.data)
            })
        }
    },
}

// mutations
const mutations = {
    setTeams(state, teams){
        state.teams = teams
    },
    setActiveIndex(state, index){
        state.activeIndex = index
    },

    setActiveMemberInfo(state, info){
        state.activeTeamInfo = info
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
