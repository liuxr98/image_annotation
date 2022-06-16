<template>
  <div>
    <div class="operation-wrap">
      <el-button type="primary" plain @click="createDialogVisible=true">
        导入模型
      </el-button>
      <div class="search-item">
        <el-input
            clearable
            suffix-icon="el-icon-search"
            v-model="search"
            placeholder="请输入模型名称"
        />
      </div>
    </div>
    <a-i-model-create-dialog :dialog-visible.sync="createDialogVisible"/>
    <a-i-model-param-edit-dialog :dialog-visible.sync="paramEditDialogVisible" :model-id="modelId"/>
    <div>
      <el-table :data="tableData">
        <el-table-column
            label="模型名称"
        >
          <template slot-scope="record">
            <el-tooltip content="点击查看模型详情">
              <router-link :to="`/model/${record.row.id}`" class="model-name-link">{{ record.row.name }}</router-link>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column label="任务状态">
          <template slot-scope="record">
            <span :style="{color: statusMap[record.row.status].color}">●&nbsp;</span>
            <span>{{statusMap[record.row.status].value}}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="record">
            <el-button type="text" @click="handleParamEdit(record.row.id)">编辑参数</el-button>
            <el-button type="text" @click="handleDelete(record.row.id)">删除</el-button>
            <el-button type="text" @click="handleTrain(record.row.id)">训练</el-button>
            <el-button type="text" @click="handleEvaluate(record.row.id)">评估</el-button>
            <el-button type="text" @click="handleExport(record.row.id)">导出</el-button>
          </template>
        </el-table-column>
      </el-table>
  </div>
  </div>
</template>

<script>
import AIModelCreateDialog from "@/components/AIModelCreateDialog";
import AIModelParamEditDialog from "@/components/AIModelParamEditDialog";
export default {
  name: "AIModelView",
  components:{
    AIModelCreateDialog,
    AIModelParamEditDialog
  },
  computed:{
    tableData(){
      return this.$store.state.model.models.filter(record => !this.search || record.name.toLowerCase().includes(this.search.toLowerCase()))
    }
  },
  data(){
    return {
      search: '',
      createDialogVisible: false,
      paramEditDialogVisible: false,
      modelId: '',
      statusMap: {
        InProgress: {
          value: '训练中',
          color: '#fa920a'
        },
        NotTrained: {
          value: '未训练',
          color: '#fa920a'
        },
        Finished:{
          value: '已完成',
          color: '#11b864'
        },
        Error: {
          value: '训练错误',
          color: '#f70000'
        }
      },

    }
  },
  created() {
    this.$store.dispatch('model/getModels')
  },
  methods:{
    handleParamEdit(id){
      this.paramEditDialogVisible = true
      this.modelId = id
    },
    handleDelete(id){
      this.$store.dispatch('model/deleteModel', id)
    },
    handleTrain(id){
      this.$store.dispatch('model/trainModel', id)
    },
    handleEvaluate(id){
      this.$store.dispatch('model/evaluateModel', id)
    },
    handleExport(id){
      let percentProgressLocal = 0
      let displayOnceFlag = false // 控制为零时进度条提醒只提醒一次

      this.$http.get(`/models/${id}/export`,{
        responseType: 'blob',
        onDownloadProgress: progressEvent => {
          let percentCompleted = Math.floor(progressEvent.loaded / progressEvent.total * 100)
          if (percentCompleted === 0 && !displayOnceFlag) {
            this.$notify({
              title: '下载正在进行中',
              message: `下载进度为${percentCompleted}%`,
              duration: 500
            })
            displayOnceFlag = true
          }
          if (percentCompleted > percentProgressLocal) {
            percentProgressLocal = percentCompleted
            if (percentCompleted % 10 === 0) {
              this.$notify({
                title: '下载正在进行中',
                message: `下载进度为${percentCompleted}%`,
                duration: 500
              });
            }
            if (percentCompleted === 100) {
              this.$message.success("下载完成")
            }
          }
        }
      }).then( response =>{
        let headers = response.headers
        let filename = ''
        let filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/
        let matches = filenameRegex.exec(headers['content-disposition']);
        if (matches != null && matches[1]) {
          filename = matches[1].replace(/['"]/g, '');
        }

        if(headers['content-type']){
          // let blob = new Blob([response.data], {type: headers['content-type']})
          let link = document.createElement('a')
          link.href = window.URL.createObjectURL(response.data)
          link.download = filename
          link.click()
        }
      })
    }
  }
}
</script>

<style scoped>
.operation-wrap{
  display: flex;
  flex-direction: row;
  align-items: center;
}
.search-item{
  width: 180px;
  margin-left: auto;
}
.model-name-link{
  color: dodgerblue;
}

</style>