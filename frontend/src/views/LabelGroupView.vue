<template>
 <div>
   <div class="operation-wrap">
     <el-button type="primary" plain @click="createDialogVisible=true">
       创建标签组
     </el-button>
     <label-group-create-dialog :dialog-visible.sync="createDialogVisible"/>

     <div class="search-item">
       <el-input
           clearable
           suffix-icon="el-icon-search"
           v-model="search"
           placeholder="请输入标签组名称"
       />
     </div>
   </div>

  <div>
    <el-table :data="tableData" >
      <el-table-column
        label="标签组名称"
        prop="name"
      />
      <el-table-column label="操作">
        <template slot-scope="record">
          <el-button type="text" @click="deleteLabelGroup(record.row.id)">删除</el-button>
          <el-divider direction="vertical"></el-divider>
          <el-button
              type="text"
              slot="reference"
              @click="editLabelDrawerVisible=true;editedLabelGroupID=record.row.id"
          >
            标签管理
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 编辑标签组 -->
    <el-drawer
        :visible.sync="editLabelDrawerVisible"
        title="标签管理"
        size="25%"
    >
      <div class="labels-wrapper">
        <div v-if="showAddLabel">
          <BaseLabelColorInput
              @cancel="showAddLabel=false"
              @change="handleAddLabelCommit"
          />
        </div>
        <div  v-else>
          <el-button type="primary" icon="el-icon-plus" plain @click="showAddLabel=true" :style="{width: 100+'%'}">
            添加标签
          </el-button>
        </div>
        <el-divider/>
        <div v-for="label in editedLabels" :key="label.id">
          <BaseLabelColorClickToEdit
              :label="label"
              class="label-item"
              :validator="editCommitValidator"
              @delete="deleteLabel(label.id)"
          />
        </div>

      </div>
    </el-drawer>
  </div>

 </div>
</template>

<script>
import LabelGroupCreateDialog from "@/components/LabelGroupCreateDialog";
import BaseLabelColorClickToEdit from "@/components/BaseLabelColorClickToEdit";
import BaseLabelColorInput from "@/components/BaseLabelColorInput";

export default {
  name: "LabelGroupView",
  components:{
    LabelGroupCreateDialog,
    BaseLabelColorClickToEdit,
    BaseLabelColorInput
  },
  data(){
    return {
      search:'',
      createDialogVisible: false,
      editLabelDrawerVisible: false,
      showAddLabel: false,
      // 被编辑的标签组ID
      editedLabelGroupID: -1,
    }
  },
  watch:{
    editedLabelGroupID(id){
      this.$store.dispatch('labelGroup/getLabelsByID', id)
    }
  },
  computed:{
    tableData(){
      return this.$store.state.labelGroup.labelGroups
              .filter(record => !this.search || record.name.toLowerCase().includes(this.search.toLowerCase()))
    },
    editedLabels(){
      return this.$store.state.labelGroup.labels
    }
  },
  methods:{
    deleteLabelGroup(labelGroupID){
      this.$store.dispatch('labelGroup/deleteLabelGroup', labelGroupID)
    },

    handleAddLabelCommit(value){
      // 在前端做一些 Check 工作: 新添加的label name不应该与已有的Label重复,以及name和color不应该为空
      if(!value.color){
        this.$message.error('颜色不能为空')
        return
      }
      if(!value.name){
        this.$message.error('标签名不能为空')
        return
      }
      for(let label of this.editedLabels){
        if(label.name === value.name){
          this.$message.error('标签名重复')
          return
        }
      }
      this.$store.dispatch('labelGroup/addLabel',{
        labelGroupID: this.editedLabelGroupID,
        label: value
      })
      this.showAddLabel = false
    },
    editCommitValidator(oldLabel, newLabel){
      // 如果修改前后的值相同，则直接返回true
      if(oldLabel.name === newLabel.name && oldLabel.color === newLabel.color){
        return [true, ""]
      }
      if(!newLabel.name){
        return [false, '标签名不应为空']
      }
      if(!newLabel.color){
        return [false, '颜色名不应为空']
      }
      for(let label of this.$store.state.labelGroup.labels){
        if(newLabel.name === label.name && newLabel.name !== oldLabel.name){
          return [false, '标签名存在冲突']
        }
      }
      this.$store.dispatch("labelGroup/updateLabel", newLabel)
      return [true, ""]
    },

    deleteLabel(labelID){
      this.$store.dispatch('labelGroup/deleteLabel', labelID)
    }
  },
  created() {
    this.$store.dispatch('labelGroup/getLabelGroups')
  }
}
</script>

<style scoped>
.operation-wrap ,.row{
  display: flex;
  flex-direction: row;
  align-items: center;
}
.search-item{
  width: 180px;
  margin-left: auto;
}
.labels-wrapper{
  width: 400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}
.label-item{
  margin-top: 15px;
  height: 50px;
}
</style>