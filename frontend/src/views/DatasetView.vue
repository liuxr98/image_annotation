<template>
 <div>
   <div class="operation-wrap">
     <el-button type="primary" plain @click="dialogVisible=true">
       创建数据集
     </el-button>
     <dataset-create-dialog :dialog-visible.sync="dialogVisible"/>
     <div class="search-item">
       <el-input
           clearable
           suffix-icon="el-icon-search"
           v-model="search"
           placeholder="请输入数据集名称"
       />
     </div>
   </div>

   <dataset-image-upload :visible.sync="imageUploadVisible" :dataset-id="importDatasetID"/>
   <dataset-label-additional-label-import :visible.sync="labelInfoUploadVisible" :dataset-id="importDatasetID"/>
   <dataset-pre-auto-annotate :visible.sync="preAutoAnnotateVisible" :dataset-id="importDatasetID"/>
   <div>
     <el-table :data="tableData">
       <el-table-column
           label="数据集名称"
           prop="name"
       />

       <el-table-column
           label="数据量"
           prop="images_cnt"
       />
      <el-table-column
        label="标注进度"
      >
         <template slot-scope="record">
           <span v-if="record.row.status === 'None'">
             <em> {{record.row.labeled_images_cnt}} / {{record.row.images_cnt}} </em>
           </span>
           <span v-else>
             {{statusMap[record.row.status]}}
           </span>
         </template>
      </el-table-column>
       <el-table-column
           label="描述"
       >
         <template slot-scope="record">
           <el-tooltip :content="record.row.description">
            <span class="text-overflow-hidden">{{record.row.description}}</span>
           </el-tooltip>
         </template>
       </el-table-column>

       <el-table-column label="操作">
         <template slot-scope="record">
           <el-button type="text" @click="handleImport(record.row.id)">导入</el-button>
           <el-button type="text" @click="handleExport(record.row.id)">导出</el-button>
           <el-button type="text" @click="handleEditView(record.row.id)">编辑查看</el-button>
           <el-dropdown style="margin-left: 10px">
             <span class="el-dropdown-link">
                更多<i class="el-icon-arrow-down el-icon--right"></i>
             </span>
             <el-dropdown-menu slot="dropdown">
               <el-dropdown-item>
                 <el-button type="text" @click="deleteDataset(record.row.id)">删除</el-button>
               </el-dropdown-item>
               <el-dropdown-item>
                 <el-button type="text" @click="handleLabelAdditionalImport(record.row.id)">自定义标签导入</el-button>
               </el-dropdown-item>
               <el-dropdown-item>
                 <el-button type="text" @click="handlePreAutoAnnotate(record.row.id)" :disabled="record.row.status !== 'None'">
                   智能预标注
                 </el-button>
               </el-dropdown-item>
             </el-dropdown-menu>
           </el-dropdown>
         </template>
       </el-table-column>
     </el-table>
   </div>
 </div>
</template>

<script>
import DatasetCreateDialog from "@/components/DatasetCreateDialog";
import DatasetImageUpload from "@/components/DatasetImageUpload";
import DatasetLabelAdditionalLabelImport from "@/components/DatasetLabelAdditionalLabelImport";
import DatasetPreAutoAnnotate from "@/components/DatasetPreAutoAnnotate";

export default {
  name: "DatasetView",
  components:{
    DatasetImageUpload,
    DatasetCreateDialog,
    DatasetLabelAdditionalLabelImport,
    DatasetPreAutoAnnotate
  },
  data(){
    return {
      search: '',
      dialogVisible: false,
      imageUploadVisible: false,
      labelInfoUploadVisible: false,
      preAutoAnnotateVisible: false,
      importDatasetID: '',
      statusMap: {
        'None': '',
        'InTeamTask': '团队任务中',
        'InAutoAnnotation': '智能预标注中'
      }
    }
  },
  computed:{
    tableData(){
      return this.$store.state.dataset.datasets.filter(record => !this.search || record.name.toLowerCase().includes(this.search.toLowerCase()))
    }
  },
  methods:{
    deleteDataset(id){
      this.$store.dispatch('dataset/deleteDataset', id)
    },
    handleImport(id){
      this.importDatasetID = id
      this.imageUploadVisible = true
    },
    handleLabelAdditionalImport(id){
      this.importDatasetID = id
      this.labelInfoUploadVisible = true
    },
    handlePreAutoAnnotate(id){
      this.importDatasetID = id
      this.preAutoAnnotateVisible = true
    },
    handleExport(id){
      let percentProgressLocal = 0
      let displayOnceFlag = false // 控制为零时进度条提醒只提醒一次
      this.$http.get(`/datasets/${id}`, {
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
      }).then(response => {
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
    },
    handleEditView(id){
      this.$router.push(`/dataset/${id}`)
    }
  },
  created() {
    this.$store.dispatch('dataset/getDatasets')
  }
}
</script>

<style scoped lang="less">
.operation-wrap{
  display: flex;
  flex-direction: row;
  align-items: center;
}
.search-item{
  width: 180px;
  margin-left: auto;
}
.text-overflow-hidden{
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>