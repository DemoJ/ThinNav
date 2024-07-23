<script setup lang="ts">
import { ref } from "vue";
import { websiteData } from "./data";
import { message } from "@/utils/message";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import AddFill from "@iconify-icons/ri/add-circle-line";

defineOptions({
  // name 作为一种规范最好必须写上并且和路由的name保持一致
  name: "Website"
});

const pagination = ref({ current: 1, pageSize: 12, total: 0 });

const onPageSizeChange = (size: number) => {
  pagination.value.pageSize = size;
  pagination.value.current = 1;
};
const onCurrentChange = (current: number) => {
  pagination.value.current = current;
};

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
    label: "描述",
    prop: "describe"
  },
  {
    label: "分类",
    prop: "category"
  },
  {
    label: "操作",
    slot: "operation"
  }
];

const handleEdit = row => {
  message(`您修改了数据`, {
    type: "success"
  });
};

const handleDelete = row => {
  message(`您删除了数据`);
};
</script>

<template>
  <el-card shadow="never">
    <div>
      <el-button :icon="useRenderIcon(AddFill)"> 新建网址 </el-button>
    </div>
    <pure-table :data="websiteData" :columns="columns">
      <template #operation="{ row }">
        <el-button size="small" @click="handleEdit(row)"> 编辑 </el-button>
        <el-button size="small" type="danger" @click="handleDelete(row)">
          删除
        </el-button>
      </template>
    </pure-table>
    <el-pagination
      v-model:currentPage="pagination.current"
      class="float-right mt-4 mb-4"
      :page-size="pagination.pageSize"
      :total="pagination.total"
      :page-sizes="[12, 24, 36]"
      :background="true"
      layout="total, sizes, prev, pager, next, jumper"
      @size-change="onPageSizeChange"
      @current-change="onCurrentChange"
    />
  </el-card>
</template>
