import { http } from "@/utils/http"; // 确保导入了正确的 http 实例
import { baseUrlApi } from "./utils";

// 上传图标
export const uploadIcon = async (formData: FormData) => {
  try {
    const response = await http.request<{ icon_url: string }>(
      "post",
      baseUrlApi("upload/upload/"),
      {
        headers: {
          "Content-Type": "multipart/form-data"
        },
        data: formData
      }
    );
    // 假设后端返回的数据格式如下
    // { "icon_url": "/uploaded_icons/filename.png" }
    return response;
  } catch (error) {
    console.error("上传图标失败:", error);
    throw error;
  }
};

// 获取图标 URL
export const getIconUrl = async (url: string) => {
  try {
    const response = await http.request<{ icon_url: string }>(
      "post",
      baseUrlApi("upload/get_icon/"),
      {
        headers: {
          "Content-Type": "application/json"
        },
        data: { url }
      }
    );

    // 假设后端返回的数据格式如下
    // { "icon_url": "http://example.com/icon.png" }
    return response;
  } catch (error) {
    console.error("获取图标失败:", error);
    throw error;
  }
};
