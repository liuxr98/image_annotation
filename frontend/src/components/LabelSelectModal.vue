<template>
  <el-card class="select-modal">
    <div slot="header">
      请选择标签
    </div>

    <div v-if="additionInfoVisible">
      <el-dialog
        :visible="visible"
        width="500px"
        @close="visible=false"
      >
        <el-form
            ref="form"
            :model="form"
            label-width="80px"
            label-position="right"
        >

          <el-form-item v-for="(format, label) in labelFormat" :key="label" :label="label">
            <el-input v-if="format.type === 'Input'" v-model="form[label]"/>
            <el-select v-else-if="format.type === 'Select'" style="width: 100%" v-model="form[label]">
              <el-option
                v-for="option in format.fields"
                :key="option"
                :value="option"
                :label="option"
              >
              </el-option>
            </el-select>
            <el-date-picker v-else style="width: 100%" v-model="form[label]">
            </el-date-picker>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="visible=false">取 消</el-button>
          <el-button type="primary" @click="handleCommit">确 定</el-button>
        </span>
      </el-dialog>
    </div>

    <el-select v-model="selectedValue" filterable placeholder="搜索关键词" @change="labelBoundingBox">
      <el-option
          v-for="item in labels"
          :key="item.id"
          :label="item.name"
          :value="item.name"
      >
      </el-option>
    </el-select>
    <el-divider/>
    <div class="button-wrapper" >
        <el-button  class="label-select-button" type="primary" @click="visible=true" v-if="additionInfoVisible" plain>添加信息</el-button>
        <el-button  class="label-select-button" type="primary" @click="deleteBoundingBox">删除标注框</el-button>
    </div>
  </el-card>
</template>

<script>
import {mapState} from "vuex";

export default {
  name: "LabelSelectModal",
  data(){
    return{
      visible: false,
      selectedValue: '',
      datasetInfo: {},
      form: Object.create(null)
    }
  },
  props:{
    bboxId:{
      required: true
    }
  },
  computed:{
    ...mapState('annotate',['labels']),
    additionInfoVisible(){
      return !!this.datasetInfo['custom_label_format']
    },
    labelFormat(){
      if(this.additionInfoVisible){
        return this.datasetInfo['custom_label_format']
      }
      return []
    }
  },
  watch:{
    visible(val){
      if(!val){
        for(let key in this.form){
          this.form[key] = ''
        }
      }
    },
    bboxId:{
      deep: true,
      handler(val){
        if(val){
          let bbox = this.$store.state.annotate.annotationBoxes.find(annotationBox => annotationBox.id === val)
          this.selectedValue = bbox.labelName
          if(bbox.additionalInfo){
            for(let key in bbox.additionalInfo){
              this.form[key] = bbox.additionalInfo[key]
            }
          }
        }
      }
    }
  },
  created() {
    let datasetId = this.$store.state.annotate.datasetID
    if(this.$store.state.annotate.datasetID){
      this.$http.get(`/datasets/info/${datasetId}`).then((response)=>{
        this.datasetInfo = response.data
      })
      for(let label in this.labelFormat){
        this.$set(this.form, label, '')
      }
    }
  },
  methods:{
    labelBoundingBox(selectedValue){
      let selectedLabel = this.labels.find(label => label.name === selectedValue)
      this.$emit("label", selectedLabel)
      // this.reset()
    },
    deleteBoundingBox(){
      this.$emit("delete")
      this.reset()
    },
    // 重置selectedLabel值
    reset(){
      this.selectedLabel = ''
    },

    handleCommit(){
      this.$emit("add-info", {...this.form})
      this.visible = false
    }
  }
}
</script>

<style scoped>
.select-modal{
  width: 180px;
}
.button-wrapper{
  width: 100%;
  display: flex;
  flex-direction: column;
}
.label-select-button{
  width: 100%;
  margin: 4px 0;
}
</style>