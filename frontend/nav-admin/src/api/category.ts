// 定义获取网址分类的函数
import { http } from "@/utils/http";
import { baseUrlApi } from "./utils";

export type CategoryResult = {
  id: number;
  name: string;
  icon_url: string;
  order: number;
  // 其他字段根据你的实际 API 返回值
};

export const getCategories = async () => {
  try {
    const data = await http.request<CategoryResult[]>("get", baseUrlApi("categories/"));
    return data;
  } catch (error) {
    console.error("Failed to fetch categories:", error);
    return [];
  }
};



