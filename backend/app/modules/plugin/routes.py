"""插件管理路由"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.response import success
from app.core.deps import get_current_user
from app.plugins.registry import list_plugins, enable_plugin, disable_plugin, run_plugin

router = APIRouter(prefix="/api/plugins", tags=["插件管理"])


@router.get("/list", summary="插件列表")
def plugin_list(_=Depends(get_current_user)):
    return success(list_plugins())


class PluginToggleIn(BaseModel):
    plugin_id: str

@router.post("/enable", summary="启用插件")
def enable(body: PluginToggleIn, _=Depends(get_current_user)):
    ok = enable_plugin(body.plugin_id)
    return success({"success": ok}, message="插件已启用" if ok else "启用失败")


@router.post("/disable", summary="禁用插件")
def disable(body: PluginToggleIn, _=Depends(get_current_user)):
    ok = disable_plugin(body.plugin_id)
    return success({"success": ok}, message="插件已禁用" if ok else "禁用失败")


class PluginRunIn(BaseModel):
    plugin_id: str
    action: str
    params: dict = {}

@router.post("/run", summary="执行插件")
def run(body: PluginRunIn, _=Depends(get_current_user)):
    result = run_plugin(body.plugin_id, body.action, body.params)
    return success(result)
