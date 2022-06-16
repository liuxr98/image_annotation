<template>
  <div id="pad" ref="pad">
    <canvas id="label-canvas" height="1000px" ref="canvas"/>

    <div
        :style="modalPosition"
        class="label-modal"
        v-show="this.selectedItemID">

      <div v-show="labelSelectModalVisible">
        <LabelSelectModal
            @delete="deleteBoundingBox"
            @label="labelBoundingBox"
            @add-info="addLabelInfo"
            :bbox-id="selectedItemID"
        />
      </div>
      <div v-show="!labelSelectModalVisible">
        <i class="el-icon-delete-solid canvas-delete-icon" @click="deleteBoundingBox"/>
      </div>
    </div>
  </div>
</template>

<script>
import {fabric} from "fabric";
import {v4 as uuidv4} from "uuid"
import LabelSelectModal from "@/components/LabelSelectModal";
import setColorOpacity from "@/util/util";
import {mapGetters, mapState} from "vuex";

// 定义 LabeledRect
fabric.LabeledRect = fabric.util.createClass(fabric.Rect, {
  type: 'labeledRect',

  initialize: function(options) {
    options || (options = { });

    this.callSuper('initialize', options);
    this.set('label', options.label || '');
  },

  toObject: function (){
    return fabric.util.object.extend(this.callSuper('toObject'), {
      label: this.get('label')
    })
  },

  _render: function(ctx){

    this.callSuper('_render', ctx)

    ctx.font = '26px Helvetica'
    ctx.fillStyle = 'rgba(255, 255, 255, 1)'
    ctx.textBaseline = 'middle' // align text vertically
    ctx.textAlign='center' // align text horizontally
    ctx.fillText(this.label, 0, 0);
  }
})
export default {
  name: "AnnotateImageCanvas",
  data(){
    return {
      isMounted: false,
      clickButton: 0,
      fabricImageObj: null, // 画布上的 fabric img 对象
      fabricCanvas: null,
      canvasCtrl: {
        isDrawing: false,
        isDragging: false,
      },
      drawingItem: null,
      selectedItemID: null,
      mouseFrom:{
        x: null,
        y: null
      },
      mouseTo:{
        x: null,
        y: null
      },
    }
  },
  components:{
    LabelSelectModal,
  },
  watch:{
    // watch to init
    imageData(val){
      if(val){
        this.fabricCanvasInit()
        this.canvasEventInit()
        this.loadBoundingBoxes()
      }
    }
  },
  computed:{
    ...mapGetters('annotate',{
      imageData: 'beingAnnotatedImage'
    }),
    ...mapState('annotate',{
      boundingBoxes: 'annotationBoxes'
    }),
    modalPosition(){
      if(this.selectedItemID) {
        let selectedItem = this.boundingBoxes.find(bbox => bbox.id === this.selectedItemID)
        let left = selectedItem.x + selectedItem.width + 20
        let top = selectedItem.y
        return {
          left: left + 'px',
          top: top + 'px'
        }
      }
      return{
        left: 0,
        top: 0,
      }
    },
    isSelectedItemLabeled(){
      if(this.selectedItemID){
        let selectedItem = this.boundingBoxes.find(bbox => bbox.id === this.selectedItemID)
        if(selectedItem.labelID){
          return true
        }
      }
      return false
    },

    labelSelectModalVisible(){
      return !this.isSelectedItemLabeled || this.clickButton === 3
    },
  },
  methods:{

    loadBoundingBoxes(){
      this.axios.get(`/datasets/images/${this.$store.getters["annotate/beingAnnotatedImageID"]}/bboxes`).then((response) =>{
        if(response.data){
          let arr = []
          for(let bbox of response.data){
            arr.push({
              id: bbox.id,
              x: bbox.factorX * this.fabricImageObj.getScaledWidth() + this.fabricImageObj.left,
              y: bbox.factorY * this.fabricImageObj.getScaledHeight() + this.fabricImageObj.top,
              width: bbox.factorWidth * this.fabricImageObj.getScaledWidth(),
              height: bbox.factorHeight * this.fabricImageObj.getScaledHeight(),
              labelID: bbox.label_info.id,
              labelName: bbox.label_info.name,
              labelColor: bbox.label_info.color
            })
          }
          this.$store.commit("annotate/setAnnotationBoxes", arr)
          this.setAnnotations()
        }
      })
    },
    setAnnotations(){
      for(let obj of this.fabricCanvas.getObjects()){
        if(obj !== this.fabricImageObj){
          this.fabricCanvas.remove(obj)
        }
      }
      this.boundingBoxes.forEach((item)=>{
        let rect = new fabric.LabeledRect({
          fill: setColorOpacity(item.labelColor, 50),
          strokeWidth: 1,
          label: item.labelName,
          left: item.x,
          top: item.y,
          width: item.width,
          height: item.height,
          id: item.id
        })
        rect.setControlsVisibility({mtr:false})
        this.fabricCanvas.add(rect)
      })
      this.fabricCanvas.renderAll()
    },

    fabricCanvasInit(){
      if(this.fabricCanvas){
        this.fabricCanvas.remove(...this.fabricCanvas.getObjects())
      }else{
        this.fabricCanvas = new fabric.Canvas('label-canvas',{
          uniformScaling: false ,// 禁用等比例缩放
          enableRetinaScaling: false,
          selection: false,
          backgroundColor: '#f7f7f7',
          fireRightClick: true, // <-- enable firing of right click events
          stopContextMenu: true, // <--  prevent context menu from showing
        })
      }

      this.fabricCanvas.setDimensions({
        width: document.getElementById('pad').clientWidth
      })

      if(this.imageData){
        let img = new Image();
        // img.setAttribute('crossOrigin','anonymous')
        img.src = this.imageData.img_src
        img.onload = () =>{
          let f_img = new fabric.Image(img)
          let scaleFactorX = this.fabricCanvas.width / f_img.width
          let scaleFactorY = this.fabricCanvas.height / f_img.height
          let scaleFactor = scaleFactorX < scaleFactorY ? scaleFactorX : scaleFactorY
          f_img.scaleToHeight(f_img.height * scaleFactor)
          f_img.scaleToWidth(f_img.width * scaleFactor)
          // 图片应该不可选中
          f_img.selectable = false
          this.fabricImageObj = f_img
          this.fabricCanvas.add(f_img)
          // 图片居中
          this.fabricCanvas.centerObject(f_img)
          this.fabricCanvas.renderAll()
        }
      }
    },

    canvasEventInit(){
      this.fabricCanvas.on({
        'mouse:down' : (e) => this.handleMouseDown(e),
        'mouse:up': (e) => this.handleMouseUp(e),
        'mouse:move' : (e) => this.handleMouseMove(e),
        'object:modified': (e) => this.handleObjectModified(e),
        'selection:created': (e) => this.handleSelectionCreated(e),
        'selection:updated': (e) => this.handleSelectionUpdated(e),
        'selection:cleared': (e) => this.handleSelectionCleared(e),
      })
    },
    isInImage(point){
      let rel = this.fabricImageObj.toLocalPoint(point, 'left', 'top')
      if(rel.x < 0 || rel.x > this.fabricImageObj.getScaledWidth() || rel.y < 0 || rel.y > this.fabricImageObj.getScaledHeight()){
        return false
      }
      return true
    },
    handleMouseDown(e){
      this.clickButton = e.button
      // 右击鼠标
      if(e.button === 3){
        if(e.target && e.target.type === "labeledRect"){
          this.selectedItemID = e.target.id
          let selectedItem = this.fabricCanvas.getObjects().find(obj => obj.id === e.target.id)
          this.fabricCanvas.setActiveObject(selectedItem)
          return
        }
      }
      if(this.selectedItemID){
        return
      }
      if(!this.isInImage(e.pointer)){
        return;
      }
      this.mouseFrom = e.pointer
      this.canvasCtrl.isDrawing = true
      let addedRect = new fabric.LabeledRect({
        fill: setColorOpacity('#91adf7', 50),
        strokeWidth: 1,
      })
      addedRect.setControlsVisibility({mtr:false})
      // addedRect.on('selected',()=>{
      //   console.log('selected')
      // })
      this.drawingItem = addedRect
      this.fabricCanvas.add(this.drawingItem)
    },
    handleMouseMove(e){
      if(!this.canvasCtrl.isDrawing){
        return
      }
      this.mouseTo = this.limitPoint(e.pointer)
      this.drawBoundingBox()
    },
    handleMouseUp(){
      //  重置
      this.canvasCtrl.isDrawing = false
      if(this.drawingItem && this.drawingItem.get('width') > 0 && this.drawingItem.get('height') > 0){
        this.drawingItem.set('id', uuidv4())
        this.$store.commit("annotate/addAnnotationBox", {
          x: this.drawingItem.get('left'),
          y: this.drawingItem.get('top'),
          width: this.drawingItem.get('width'),
          height: this.drawingItem.get('height'),
          id: this.drawingItem.get('id'),
          labelColor: '#91adf7',
        })
      }
      this.drawingItem = null
    },
    handleSelectionCreated(){
      this.selectedItemID = this.fabricCanvas.getActiveObject().get("id")
    },
    handleSelectionCleared(){
      this.selectedItemID = null
    },
    handleSelectionUpdated(){
      this.selectedItemID = this.fabricCanvas.getActiveObject().get("id")

    },

    handleObjectModified(e){
      // 行为处理参考了 CVAT(Computer Vision Annotation Tool)
      let modifiedItem = e.target
      let id = modifiedItem.get('id')
        // TopLeft Pos
        let curTLPos = new fabric.Point(
          modifiedItem.get('left'),
          modifiedItem.get('top')
        )

        // TopRight Pos
        let curTRPos = new fabric.Point(
          modifiedItem.get('left') + modifiedItem.getScaledWidth(),
          modifiedItem.get('top')
        )

        // BottomLeft Pos
        let curBLPos = new fabric.Point(
          modifiedItem.get('left'),
          modifiedItem.get('top') + modifiedItem.getScaledHeight()
        )

        // BottomRight Pos
        let curBRPos = new fabric.Point(
          modifiedItem.get('left') + modifiedItem.getScaledWidth(),
          modifiedItem.get('top') + modifiedItem.getScaledHeight()
        )

        // 如果整个 bounding box 都不在图片上 则撤销该操作
        if(!this.isInImage(curTLPos) && !this.isInImage(curTRPos) && !this.isInImage(curBLPos) && !this.isInImage(curBRPos)){
          modifiedItem.set({
            left: e.transform.original.left,
            top: e.transform.original.top
          })
        }else {
          // 否则以图片边界来截断选择框
          let newTLPos = this.limitPoint(curTLPos)
          let newBRPos = this.limitPoint(curBRPos)
          this.setRect(
              modifiedItem,
              newTLPos.x,
              newTLPos.y,
              // 需要减去 strokeWidth 否则会越移动越大，原因可能是因为 getScaledHeight/getScaledWidth 计算包括 strokeWidth
              newBRPos.x - newTLPos.x - modifiedItem.strokeWidth,
              newBRPos.y - newTLPos.y - modifiedItem.strokeWidth
          )

          this.$store.commit("annotate/updateAnnotationBox", {
            id: id,
            patchedObj:{
              x: newTLPos.x,
              y: newTLPos.y,
              width: newBRPos.x - newTLPos.x - modifiedItem.strokeWidth,
              height: newBRPos.y - newTLPos.y - modifiedItem.strokeWidth
            }
          })
        }
    },

    drawBoundingBox(){
      if(this.drawingItem){
      let x = this.mouseFrom.x < this.mouseTo.x ? this.mouseFrom.x : this.mouseTo.x
      let y = this.mouseFrom.y < this.mouseTo.y ? this.mouseFrom.y : this.mouseTo.y
      let width = Math.abs(this.mouseTo.x - this.mouseFrom.x)
      let height = Math.abs(this.mouseTo.y - this.mouseFrom.y)
       this.drawingItem.set({
         left: x,
         top: y,
         width: width,
         height: height
       })
        this.drawingItem.setCoords()
        this.fabricCanvas.renderAll()
      }
    },

    setRect(rect, x, y, width, height){
      rect.set({
        left: x,
        top: y,
        width: width,
        height: height,
        scaleX: 1,
        scaleY: 1
      })
      // 改变 top 以及 left后，必须调用此方法，否则无法选中
      rect.setCoords()
    },

    // 限制图片之外的移动
    limitPoint(point){
      let rel = this.fabricImageObj.toLocalPoint(point, 'left', 'top')
      let res = {x: point.x, y: point.y}

      if(rel.x < 0){
        res.x = this.fabricImageObj.left
      }
      if(rel.x > this.fabricImageObj.getScaledWidth()){
        res.x = this.fabricImageObj.left + this.fabricImageObj.getScaledWidth()
      }
      if(rel.y < 0){
        res.y = this.fabricImageObj.top
      }
      if(rel.y > this.fabricImageObj.getScaledHeight()){
        res.y = this.fabricImageObj.top + this.fabricImageObj.getScaledHeight()
      }
      return res
    },
    deleteBoundingBox(){
      let selected = this.fabricCanvas.getActiveObject()
      if(selected){
        let selectedID = selected.get("id")
        this.$store.commit("annotate/deleteAnnotationBox", selectedID)
        this.fabricCanvas.remove(selected)
      }
    },
    labelBoundingBox(v){
      let select = this.fabricCanvas.getActiveObject()
      let label = this.$store.state.annotate.labels.find(item => item.name === v.name)
      let selectedID = select.get("id")
      this.$store.commit("annotate/updateAnnotationBox", {
        id: selectedID,
        patchedObj: {
          labelColor: label.color,
          labelName: label.name,
          labelID: label.id
        }
      })
      select.set({
        // set dirty to true to render, refer https://stackoverflow.com/questions/56897837/fabric-js-requestrenderall-method-vs-renderall-method
        dirty: true,
        label: label.name,
        fill: setColorOpacity(label.color, 50)
      })
      let backup = this.selectedItemID
      // 这边是为了使计算属性中的isSelectedLabel重新Evaluate
      this.selectedItemID = null
      this.selectedItemID = backup
      this.fabricCanvas.renderAll()
    },
    addLabelInfo(additionalInfo){
      let select = this.fabricCanvas.getActiveObject()
      let selectedID = select.get("id")
      this.$store.commit("annotate/updateAnnotationBox", {
        id: selectedID,
        patchedObj: {
         additionalInfo: additionalInfo
        }
      })
    },
  },

  created() {
    this.unsubscribeAction = this.$store.subscribeAction((action)=>{
      if(action.type === 'annotate/saveAll'){
        let committed = []
        for(let bbox of this.boundingBoxes){
          let _bbox = {}
          // 将 canvas 坐标系的标注框转化为图片坐标系
          let rel = this.fabricImageObj.toLocalPoint(new fabric.Point(bbox.x, bbox.y))
          _bbox.factorX = rel.x / this.fabricImageObj.getScaledWidth()
          _bbox.factorY = rel.y / this.fabricImageObj.getScaledHeight()
          _bbox.factorWidth = bbox.width / this.fabricImageObj.getScaledWidth()
          _bbox.factorHeight = bbox.height / this.fabricImageObj.getScaledHeight()
          _bbox.dataset_label_id = bbox.labelID
          // _bbox.type = this.$store.state.annotate.taskType === taskTypes.TeamWork ? 1 : 0,
          _bbox.additionalInfo = bbox.additionalInfo
          committed.push(_bbox)
        }
        this.$store.dispatch('annotate/saveAnnotationBoxes', committed)
      }
    })
    this.unsubscribe = this.$store.subscribe((mutation) => {
      if(mutation.type === 'annotate/redraw'){
        this.setAnnotations()
      }
    })
  },
  beforeDestroy() {
    this.unsubscribeAction()
    this.unsubscribe()
  },
}
</script>

<style scoped>
#pad{
  position: relative;
  width: 100%;
}
#label-canvas{
}
.label-modal{
  position: absolute;
  left: 0;
  top:  0;
}
.canvas-delete-icon{
  cursor: pointer;
  font-size: 25px;
}
</style>