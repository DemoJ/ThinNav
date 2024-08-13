<script setup lang="tsx">
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import AddFill from "@iconify-icons/ri/add-circle-line";
import { getCategories } from "@/api/category";
import { onMounted, ref } from "vue";
import {
  handleEdit,
  handleDelete,
  handleCreat,
  setFetchCategoriesMethod
} from "./cateOperate";

defineOptions({
  // name 作为一种规范最好必须写上并且和路由的name保持一致
  name: "Category"
});

const categoryData = ref([]);

const fetchCategories = async () => {
  categoryData.value = await getCategories();
};

// 页面挂载时获取数据并设置 fetchCategories 方法
onMounted(() => {
  fetchCategories();
  setFetchCategoriesMethod(fetchCategories); // 设置 fetchCategories 方法
});

const columns: TableColumnList = [
  {
    label: "名称",
    prop: "name"
  },
  {
    label: "图标",
    prop: "icon_url"
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
</script>

<template>
  <el-card shadow="never">
    <div>
      <el-button :icon="useRenderIcon(AddFill)" @click="handleCreat()">
        新建分类
      </el-button>
    </div>
    <pure-table :data="categoryData" :columns="columns">
      <template #operation="{ row }">
        <el-button size="small" @click="handleEdit(row)">编辑</el-button>
        <el-button size="small" type="danger" @click="handleDelete(row)">
          删除
        </el-button>
      </template>
    </pure-table>
  </el-card>
</template>
