"""预置厂商配置（兼容OpenAI协议）"""

PRESET_PROVIDERS = {
    "openai": {
        "provider_name": "OpenAI (GPT)",
        "base_url": "https://api.openai.com/v1",
        "default_model": "gpt-4o-mini",
    },
    "doubao": {
        "provider_name": "字节跳动 豆包",
        "base_url": "https://ark.cn-beijing.volces.com/api/v3",
        "default_model": "doubao-pro-4k",
    },
    "deepseek": {
        "provider_name": "深度求索 DeepSeek",
        "base_url": "https://api.deepseek.com/v1",
        "default_model": "deepseek-chat",
    },
    "qwen": {
        "provider_name": "阿里 通义千问",
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "default_model": "qwen-plus",
    },
    "zhipu": {
        "provider_name": "智谱AI GLM",
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "default_model": "glm-4-flash",
    },
    "moonshot": {
        "provider_name": "月之暗面 Kimi",
        "base_url": "https://api.moonshot.cn/v1",
        "default_model": "moonshot-v1-8k",
    },
}
