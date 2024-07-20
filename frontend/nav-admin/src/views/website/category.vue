<script setup lang="ts">
import { message } from "@/utils/message";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import AddFill from "@iconify-icons/ri/add-circle-line";
import { getCategories } from "@/api/category";
import { onMounted, ref } from "vue";


defineOptions({
  // name 作为一种规范最好必须写上并且和路由的name保持一致
  name: "Category"
});


const categoryData = ref([]);

const columns: TableColumnList = [
  {
    label: "名称",
    prop: "name"
  },
  {
    label: "排序",
    prop: "order"
  },
  {
    label: "操作",
    slot: "operation"
  }
];

const handleEdit = (row) => {
    message(`您修改了数据`, {
      type: "success"
    });
  };

  const handleDelete = (row) => {
    message(`您删除了数据`);
  };

  // 页面挂载时执行操作
  onMounted(async () => {
    categoryData.value = await getCategories();
    // console.log(categoryData.value);
  });
</script>

<template>
  <el-card shadow="never">
    <div>
    <el-button :icon="useRenderIcon(AddFill)">
        新建分类
      </el-button>
      </div>
    <pure-table :data="categoryData" :columns="columns" >
      <template #operation="{ row }" >
        <el-button size="small" @click="handleEdit(row)">
          编辑
        </el-button>
        <el-button size="small" type="danger" @click="handleDelete(row)">
          删除
        </el-button>
      </template>
    </pure-table>
  </el-card>
</template>