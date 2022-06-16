<template>
 <div class="content-wrapper">
   <div class="control-bar">
     <el-button
         :disabled="deleteButtonDisable"
         type="text"
         icon="el-icon-delete"
         @click="handleDelete"
     >
       删除
     </el-button>
      <div v-if="selectedTextVisible">
        <el-divider direction="vertical"/>
        已选择<em style="color: #f39000">&ensp;{{selectedLength}}&ensp;</em>个
      </div>
   </div>
   <div id="entity-list">
      <DatasetImageItem
        v-for="image in images"
        :key="image.id"
        :img="image"
        @select="handleSelect"
        @cancel-select="handleCancelSelect"
      />
   </div>
 </div>
</template>

<script>
import Vue from "vue";
import DatasetImageItem from "@/components/DatasetImageItem";

export default {
  name: "DatasetImageView",
  data(){
    return {
      images: [],
      selected: []
    }
  },
  computed:{
    selectedTextVisible(){
      return this.selectedLength !== 0
    },
    selectedLength(){
      return this.selected.length
    },
    deleteButtonDisable(){
      return this.selectedLength === 0
    }
  },
  components:{
    DatasetImageItem
  },
  methods:{
    handleSelect(id){
      this.selected.push(id)
    },
    handleCancelSelect(id){
      let deletedIndex = this.selected.findIndex(itemID => itemID === id)
      this.selected.splice(deletedIndex, 1)
    },
    handleDelete(){
      this.$http.delete(`/datasets/${this.$route.params.id}/images`, {
        data:{
          deletedIndexArray: this.selected
        }
      }).then(()=>{
        this.selected = []
        this.loadData()
      })
    },
    loadData(){
      Vue.axios.get(`/datasets/${this.$route.params.id}/images`).then(response =>{
        this.images = response.data.map(image => {
          if(!image.img_src.startsWith('http')){
            image.img_src = process.env.VUE_APP_BASEURL + '/data/' +  image.img_src
          }
          return image
        })
      })
    }
  },
  created() {
   this.loadData()
  }
}
</script>

<style scoped lang="less">
.content-wrapper{
  display: flex;
  flex-direction: column;
}
.control-bar{
  height: 60px;
  align-items: center;
  flex-shrink: 0;
  flex-grow: 0;

  display: flex;
}
#entity-list{
  max-height: 80vh;
  overflow-y: auto;

  display: flex;
  flex-wrap: wrap;
  align-content: flex-start;
}
</style>