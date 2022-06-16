<template>
  <el-menu router :default-openeds="['/labeling']" :default-active="'/'+$route.path.split('/')[1]" class="menu">
    <el-submenu index="/labeling">
      <template slot="title">
        <span>数据标注管理</span>
      </template>
      <el-menu-item index="/dataset">数据集</el-menu-item>
      <el-menu-item index="/label-groups">标签组</el-menu-item>
      <el-menu-item index="/annotate">在线标注</el-menu-item>
      <el-menu-item index="/task">多人标注</el-menu-item>
      <el-menu-item index="/team">标注团队管理</el-menu-item>
    </el-submenu>
    <el-menu-item index="/model">
      模型管理
    </el-menu-item>
    <el-menu-item index="/detect">
      目标检测
    </el-menu-item>
  </el-menu>
</template>

<script>
export default {
  name: "TheSidebar"
}
</script>

<style scoped>

</style>