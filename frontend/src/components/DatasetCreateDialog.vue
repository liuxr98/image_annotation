<template>
  <el-dialog
      :visible="dialogVisible"
      title="创建数据集"
      width="500px"
      @close="handleClose"
  >
    <el-form
        ref="form"
        :model="form"
        :rules="rules"
        label-position="right"
        label-width="120px"
    >
      <el-form-item label="数据集名称" prop="name">
        <el-input v-model="form.name" :maxlength="30"></el-input>
      </el-form-item>
      <el-form-item label="描述" prop="description">
        <el-input v-model="form.description"></el-input>
      </el-form-item>
<!--      <el-form-item label="样本">-->
<!--        <el-upload-->
<!--            class="upload-demo"-->
<!--            action="https://jsonplaceholder.typicode.com/posts/"-->
<!--            multiple-->
<!--            :limit="3"-->
<!--            :file-list="fileList">-->
<!--          <el-button size="small" type="primary">点击上传</el-button>-->
<!--        </el-upload>-->
<!--      </el-form-item>-->

    </el-form>
     <span slot="footer" class="dialog-footer">
      <el-button @click="handleClose">取 消</el-button>
      <el-button type="primary" @click="handleCommit">确 定</el-button>
    </span>
  </el-dialog>
</template>

<script>
export default {
  name: "DatasetCreateDialog",
  props: {
    dialogVisible: {
      type: Boolean,
      default: false,
    }
  },
  data(){
    let nameDuplicateValidator = (rule, value, callback) =>{
      for(let dataset of this.$store.state.dataset.datasets){
        if(dataset.name === value){
          callback(new Error('数据集名称重复,请修改'))
        }
      }
      callback()
    }
    return {
      form:{
        name: '',
        description: '',
      },
      // fileList: [{name: 'food.jpeg', url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'}, {name: 'food2.jpeg', url: 'https://fuss10.elemecdn.com/3/63/4e7f3a15429bfda99bce42a18cdd1jpeg.jpeg?imageMogr2/thumbnail/360x360/format/webp/quality/100'}],
      rules: {
        name: [
          {required: true, message: '请输入数据集名称', trigger: 'blur'},
          {validator: nameDuplicateValidator, trigger: 'blur'}
        ]
      }
    }
  },
  watch:{
    dialogVisible(val){
      if(!val){
        // 清除验证信息
        this.$refs.form.resetFields()
        // 重置数据
        this.resetFormData()
      }
    }
  },
  methods:{
    handleCommit() {
      this.$refs.form.validate((valid)=>{
        if(valid){
          this.$store.dispatch('dataset/addDataset', this.form)
          this.handleClose()
        }
      })
    },

    handleClose(){
      this.$emit('update:dialogVisible', false);
    },

    resetFormData(){
      this.form = {
        name: '',
        description: '',
      }
    }
  }
}
</script>

<style scoped>

</style>