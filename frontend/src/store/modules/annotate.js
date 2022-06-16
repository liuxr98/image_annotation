import Vue from "vue";
import {taskTypes} from "@/util/enum";
const state = () => ({
    datasetID: '', // 当前正在标注的数据集ID
    taskType: taskTypes.Annotate,
    labels: [] ,// 与当前数据集绑定的标签
    images: [] ,//当前数据集的所有图片
    category: 'Unlabeled', // 可能值为 All, Unlabeled, Labeled
    activeIndex: 0, // 正在标注的图片在thumbnailImageList中的位置,
    annotationBoxes: [], // 正在标注的图片的所有标注框
    subtaskID: '',
    teamTaskID: ''
})

// getters
const getters = {
    // 在thumbnail显示的图片列表
    thumbnailImageList: (state) =>{
        if(state.category === 'All'){
            return state.images
        }else if(state.category === 'Unlabeled'){
            return state.images.filter(image => !image.labeled)
        }else{
            return state.images.filter(image => image.labeled)
        }
    },

    thumbnailImageListLength: (state, getters) =>{
        return getters.thumbnailImageList.length
    },

    beingAnnotatedImage: (state, getters) => {
        if(getters.thumbnailImageListLength !== 0) {
            return getters.thumbnailImageList[state.activeIndex]
        }
        return ""
    },

    beingAnnotatedImageID: (state, getters) => {
        if(getters.beingAnnotatedImage){
            return getters.beingAnnotatedImage.id
        }
        return ""
    },
}


// actions
const actions= {
    /*
        @desc 初始化标注页面相关数据
     */
    initAnnotate({dispatch, commit, state}){
        if(state.taskType === taskTypes.Review){
            commit('setCategory', 'All')
        }else{
            commit('setCategory', 'Unlabeled')
        }
        commit('setActiveIndex', 0)
        dispatch('getLabels')
        dispatch('getImages')
    },


    getImages({commit, state}){
        if(state.taskType === taskTypes.TeamWork){
            Vue.axios.get(`/teamtasks/subs/${state.subtaskID}/images`).then(response =>{
                commit('setImages', response.data)
            })
        }else if(state.taskType === taskTypes.Annotate){
            Vue.axios.get(`/datasets/${state.datasetID}/images`).then(response => {
                commit('setImages', response.data)
            })
        }else{
            Vue.axios.get(`/teamtasks/${state.teamTaskID}/images`).then(response=>{
                commit('setImages', response.data)
            })
        }

    },

    getLabels({commit, state}) {
        Vue.axios.get(`/datasets/${state.datasetID}/labels`).then(response =>{
            commit('setLabels', response.data)
        })
    },

    /*
        @desc 为当前数据集添加单个标签
    */
    addLabel({state, dispatch}, label){
        Vue.axios.post(`/datasets/${state.datasetID}/labels`, {
            labelGroupImportFlag: false,
            label: label
        }).then(()=>{
            dispatch('getLabels')
        })
    },

    /*
        @desc 为当前数据集导入标签组
    */
    addLabels({state}, labelGroupID){
        // 返回 Promise 用于在组件中使用，从而获取导入标签组与已有标签的冲突值
        return new Promise((resolve, reject)=>{
            Vue.axios.post(`/datasets/${state.datasetID}/labels`, {
                labelGroupImportFlag: true,
                labelGroupID: labelGroupID
            }).then((response) =>{
                resolve(response)
            }).catch((error) => {
                reject(error)
            })
        })
    },

     deleteLabel({dispatch, commit},deletedLabelID){
         Vue.axios.delete(`/datasets/labels/${deletedLabelID}`)
         .then(() =>{
            commit('deleteAnnotationBoxByLabel', deletedLabelID)
            commit('redraw')
            dispatch("getLabels")
         })
    },

    updateLabel({dispatch, commit}, label){
        Vue.axios.put(`/datasets/labels/${label.id}`, label)
        .then(()=>{
            commit('updateAnnotationBoxByLabel', label)
            commit('redraw')
            dispatch("getLabels")
        })
    },

    /*
        @desc 用于被监听从而触发更换图片后对标注框的提交
     */
    saveAll(){
    },

    /*
        @desc
     */
    checkAndSave({state, dispatch}){
        return new Promise((resolve) => {
            let checkState = true
            // 检查是否有标签没有标注框
            for(let annotationBox of state.annotationBoxes){
                if(!annotationBox.labelName){
                    checkState = false
                    break
                }
            }
            if(checkState){
                dispatch("saveAll")
                resolve(true)
            }else{
                resolve(false)
            }
        })
    },



    /*
        @desc 用于主动调用来提交当前图片的所有标注
     */
    saveAnnotationBoxes({getters}, bboxes){
        Vue.axios.post(`/datasets/images/${getters.beingAnnotatedImageID}/bboxes`, bboxes).then(()=>{
        })
    },

    reviewTeamTaskInAnnotate({dispatch, state}){
        dispatch("teamTask/reviewTeamTask", state.teamTaskID, {root: true} )
    }
}

// mutations
const mutations = {
    /*
        @desc 设置标注的数据集ID
     */
    setDatasetID(state, datasetID){
        state.datasetID = datasetID
    },

    setLabels(state, labels){
        state.labels = labels
    },


    setImages(state, images){
        state.images = images.map(image => {
            if(!image.img_src.startsWith('http')){
                image.img_src = process.env.VUE_APP_BASEURL + '/data/' + image.img_src
            }
            return image
        })
    },


    /*
        @desc 设置正在标注的图片在thumbnailImageList中的位置
    */
    setActiveIndex(state, index){
        state.activeIndex = index
    },

    setAnnotationBoxes(state, annotationBoxes){
        state.annotationBoxes = annotationBoxes
    },

    addAnnotationBox(state, annotationBox){
        state.annotationBoxes.push(annotationBox)
    },

    /*
        @desc 更新标注框
        @param {Object} payload
            {
                id: ...
                patchedObj: ...
            }
     */
    updateAnnotationBox(state, payload){
        let updatedAnnotationBox = state.annotationBoxes.find(annotationBox => annotationBox.id === payload.id)
        Object.assign(updatedAnnotationBox, payload.patchedObj)
    },

    /*
        @desc 根据id删除标注框
     */
    deleteAnnotationBox(state, id){
        let deletedIndex = state.annotationBoxes.findIndex(annotationBox => annotationBox.id === id)
        state.annotationBoxes.splice(deletedIndex, 1)
    },

    /*
        @desc 根据标签ID来删除标注框
     */
    deleteAnnotationBoxByLabel(state, labelID){
        for(let i = 0; i < state.annotationBoxes.length; i++){
            if(state.annotationBoxes[i].labelID && state.annotationBoxes[i].labelID === labelID){
                state.annotationBoxes.splice(i, 1)
                i--
            }
        }
    },

    /*
        @desc 根据标签来更新标注框
     */
    updateAnnotationBoxByLabel(state, label){
        for(let i = 0; i < state.annotationBoxes.length; i++){
            if('labelID' in state.annotationBoxes[i] && state.annotationBoxes[i].labelID === label.id){
                Object.assign(state.annotationBoxes[i], {
                    labelName: label.name,
                    labelColor: label.color
                })
            }
        }
    },

    /*
       @desc 用于被监听从而触发删除或更新标签后,重画标注框
     */
    redraw(){
    },

    setCategory(state, category){
        state.category = category
    },

    setTaskType(state, type){
        state.taskType = type
    },

    setSubtaskID(state, id){
      state.subtaskID = id
    },

    setTeamTaskID(state, id){
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