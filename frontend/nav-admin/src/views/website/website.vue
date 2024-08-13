<script setup lang="ts">
import { ref, onMounted, watch } from "vue";
import { getWebs } from "@/api/website";
import { useRenderIcon } from "@/components/ReIcon/src/hooks";
import AddFill from "@iconify-icons/ri/add-circle-line";
import {
  handleEdit,
  handleDelete,
  handleCreat,
  setFetchWebsMethod
} from "./webOperate";

defineOptions({
  // name 作为一种规范最好必须写上并且和路由的name保持一致
  name: "Website"
});

const webData = ref([]);
const pagination = ref({ current: 1, pageSize: 10, total: 0 });

const fetchWebs = async () => {
  const { data, total } = await getWebs({
    page: pagination.value.current || 1, // 确保 page 为有效数字
    limit: pagination.value.pageSize || 10 // 确保 limit 为有效数字
  });
  webData.value = data;
  pagination.value.total = total;
};

// 页面挂载时获取数据
onMounted(() => {
  fetchWebs();
  setFetchWebsMethod(fetchWebs); // 设置 fetchWebs 方法
});

// 监听分页参数变化，重新获取数据
watch(
  [() => pagination.value.current, () => pagination.value.pageSize],
  fetchWebs
);

const onPageSizeChange = (size: number) => {
  pagination.value.pageSize = size || 10; // 默认为10
  pagination.value.current = 1;
};

const onCurrentChange = (current: number) => {
  pagination.value.current = current || 1; // 默认为1
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
    prop: "description"
  },
  {
    label: "分类",
    prop: "category_name"
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
        新建网址
      </el-button>
    </div>
    <pure-table :data="webData" :columns="columns">
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
      :page-sizes="[10, 20, 50]"
      :background="true"
      layout="total, sizes, prev, pager, next, jumper"
      @size-change="onPageSizeChange"
      @current-change="onCurrentChange"
    />
  </el-card>
</template>
