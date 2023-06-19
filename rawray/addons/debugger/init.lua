local _main
local deadlock_disabled = false

local debugger = {
	name = "debugger",
	
	all_loaded = function()
		if not rr.config or not rr.config.debugger or not rr.config.debugger.enable then
			deadlock_disabled = true -- don't disable deadlock
			return
		end

		local address = rr.config.debugger["address"] or "127.0.0.1:12302"

		local compat_mode = true
		if package.preload["thread.exdata2"] then
			compat_mode = false
			rr.log_info("debugger running on new/modded luajit version")
		else
			rr.log_info("debugger running in compatibility mode")
		end

		--[[ HACK: pass luajit detection, TODO: modify the detection

			if (tostring(assert):match('builtin') ~= nil) then
            	rt = rt.."/luajit"
		--]]
		local rawtostring = tostring
		tostring = function (val)
			if val == assert then
				return 'builtin'
			end
			return rawtostring(val)
		end

		local debugger_path = (compat_mode and "/addons/debugger/dbg_compat") or "/addons/debugger/dbg_modded"
		_main = rr.dofile("addons/debugger/debugger.lua")(rr.root_dir..debugger_path)
		local dbg = _main:start(address)
		tostring = rawtostring
		if compat_mode then
		-- dbg:setup_patch() uncaught exceptions cause the game to pause, disable for now til it's fixed
		-- this is still an issue when using modded luajit
		end
		dbg:event("wait")
	end,
	
	update = function(dt)
		if not deadlock_disabled then
			s3d.Deadlock.pause()
			deadlock_disabled = true
		end
	end,

	-- unload = function ()
	-- 	-- s3d.Deadlock.unpause()
	-- end
}

return debugger