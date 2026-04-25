/*
 * Owais Launcher
 * Modification of Zalith Launcher 2 (GPL-3.0).
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 */

package com.movtery.zalithlauncher.game.version.mod

import com.movtery.zalithlauncher.utils.logging.Logger.lInfo
import com.movtery.zalithlauncher.utils.logging.Logger.lWarning
import java.io.File
import java.nio.file.Files
import java.nio.file.StandardCopyOption

/**
 * Removes duplicate mods (mods sharing the same mod ID, e.g. two versions of Sodium)
 * from the mods directory, keeping only the newest by file modified time.
 * Older versions are moved into a sibling `mods_backup/` folder for easy rollback.
 */
object ModDeduplicator {

    /**
     * @return file names of mods that were moved to backup (empty if none)
     */
    fun deduplicate(modsDir: File, mods: List<LocalMod>): List<String> {
        if (mods.size <= 1) return emptyList()

        val groups = mods
            .filter { !it.notMod && it.id.isNotBlank() }
            .groupBy { it.id }

        val backupDir = File(modsDir.parentFile ?: modsDir, "mods_backup")
        val removed = mutableListOf<String>()

        for ((modId, group) in groups) {
            if (group.size <= 1) continue

            val sorted = group.sortedByDescending { it.file.lastModified() }
            val keep = sorted.first()
            val toMove = sorted.drop(1)

            if (toMove.isNotEmpty() && !backupDir.exists()) {
                backupDir.mkdirs()
            }

            for (mod in toMove) {
                val src = mod.file
                if (!src.exists()) continue
                val dest = uniqueDest(backupDir, src.name)
                try {
                    Files.move(
                        src.toPath(),
                        dest.toPath(),
                        StandardCopyOption.REPLACE_EXISTING
                    )
                    removed.add(src.name)
                    lInfo("Dedup: moved ${src.name} (mod id=$modId) to backup, kept ${keep.file.name}")
                } catch (e: Exception) {
                    lWarning("Dedup: failed to move ${src.name} to backup", e)
                }
            }
        }

        return removed
    }

    private fun uniqueDest(dir: File, name: String): File {
        var dest = File(dir, name)
        if (!dest.exists()) return dest
        val base = name.substringBeforeLast('.', name)
        val ext = name.substringAfterLast('.', "")
        var i = 1
        while (dest.exists()) {
            val newName = if (ext.isNotEmpty() && ext != name) "$base.$i.$ext" else "$base.$i"
            dest = File(dir, newName)
            i++
        }
        return dest
    }
}
