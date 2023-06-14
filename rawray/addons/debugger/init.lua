local _main
local is_set = false

local debugger = {
	name = "debugger",
	
	all_loaded = function()
		if not rr.config or not rr.config.debugger or not rr.config.debugger.enable then
			is_set = true -- don't disable deadlock
			return
		end
		local address = "127.0.0.1:12302"
		if rr.config and rr.config.debugger then
			address = rr.config.debugger["address"] or address
		end
		
		if not package.preload["thread.exdata2"] then
			s3d.Application.quit_with_message("RawRay debugger running on non modded luajit, Unstable!\nDisable debugger in config.lua or install debugger with _Debugger_Install_LuaJIT.bat")
			return
		end
		--[[ HACK: pass luajit detection, TODO: modify the detection

			if (tostring(assert):match('builtin') ~= nil) then
            	rt = rt.."/luajit"
		--]]
		local og_tostring = tostring
		tostring = function (val)
			if val == assert then
				return 'builtin'
			end
			return og_tostring(val)
		end
		_main = rr.dofile("addons/debugger/debugger.lua")
		local dbg = _main:start(address)
		tostring = og_tostring
		dbg:event("wait")
	end,
	
	update = function(dt)
		if not is_set then --disable deadlock detector
			s3d.Deadlock.pause()
			s3d.Deadlock.pause = function() end
			s3d.Deadlock.unpause = function() end
			is_set = true
		end
	end,
}

return debugger