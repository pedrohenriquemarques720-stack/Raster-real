// AudioHapticManager.kt - Gerenciador de Áudio e Vibração

package com.autelpro.audio

import android.content.Context
import android.media.AudioAttributes
import android.media.MediaPlayer
import android.media.SoundPool
import android.os.Build
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import kotlinx.coroutines.*

class AudioHapticManager(private val context: Context) {
    
    // SoundPool para áudios curtos
    private val soundPool: SoundPool
    private val soundMap = mutableMapOf<SoundType, Int>()
    
    // Vibrator para feedback tátil
    private val vibrator: Vibrator
    
    // Dispatcher para operações assíncronas
    private val scope = CoroutineScope(Dispatchers.IO + SupervisorJob())
    
    // MediaPlayer para áudios longos (opcional)
    private var mediaPlayer: MediaPlayer? = null
    
    enum class SoundType {
        ALERT_CRITICAL,     // Falha grave
        SGW_UNLOCK,         // Desbloqueio de gateway
        SCAN_COMPLETE,      // Scan concluído
        SUCCESS,            // Operação bem-sucedida
        ERROR,              // Erro
        CONNECTION          // Conexão estabelecida
    }
    
    enum class HapticType {
        SHORT_PULSE,        // Pulso curto
        DOUBLE_PULSE,       // Pulso duplo
        LONG_PULSE,         // Pulso longo
        SUCCESS_PATTERN,    // Padrão de sucesso
        ERROR_PATTERN,      // Padrão de erro
        TICK                // Toque leve
    }
    
    init {
        // Inicializa SoundPool (compatível com todas as versões)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.LOLLIPOP) {
            val audioAttributes = AudioAttributes.Builder()
                .setUsage(AudioAttributes.USAGE_ASSISTANCE_SONIFICATION)
                .setContentType(AudioAttributes.CONTENT_TYPE_SONIFICATION)
                .build()
            
            soundPool = SoundPool.Builder()
                .setMaxStreams(5)
                .setAudioAttributes(audioAttributes)
                .build()
        } else {
            @Suppress("DEPRECATION")
            soundPool = SoundPool(5, android.media.AudioManager.STREAM_MUSIC, 0)
        }
        
        // Carrega sons
        loadSounds()
        
        // Inicializa vibrator
        vibrator = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            val vibratorManager = context.getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as VibratorManager
            vibratorManager.defaultVibrator
        } else {
            @Suppress("DEPRECATION")
            context.getSystemService(Context.VIBRATOR_SERVICE) as Vibrator
        }
    }
    
    private fun loadSounds() {
        // Em um app real, carregue arquivos de som da pasta raw
        // soundMap[SoundType.ALERT_CRITICAL] = soundPool.load(context, R.raw.alert_critical, 1)
        // soundMap[SoundType.SGW_UNLOCK] = soundPool.load(context, R.raw.sgw_unlock, 1)
        // soundMap[SoundType.SCAN_COMPLETE] = soundPool.load(context, R.raw.scan_complete, 1)
        
        // Simulação com sons do sistema
        soundMap[SoundType.ALERT_CRITICAL] = 1
        soundMap[SoundType.SGW_UNLOCK] = 2
        soundMap[SoundType.SCAN_COMPLETE] = 3
        soundMap[SoundType.SUCCESS] = 4
        soundMap[SoundType.ERROR] = 5
    }
    
    /**
     * Toca um som específico com vibração associada
     */
    fun playSound(soundType: SoundType, hapticType: HapticType? = null) {
        scope.launch {
            // Toca o som
            soundMap[soundType]?.let { soundId ->
                soundPool.play(soundId, 1.0f, 1.0f, 1, 0, 1.0f)
            }
            
            // Vibra se solicitado
            hapticType?.let {
                vibrate(it)
            }
        }
    }
    
    /**
     * Gatilho para falha grave encontrada
     * Som de alerta técnico e vibração curta dupla
     */
    fun triggerCriticalFault() {
        playSound(SoundType.ALERT_CRITICAL, HapticType.DOUBLE_PULSE)
    }
    
    /**
     * Gatilho para desbloqueio de Security Gateway
     * Som de sucesso tecnológico (cofre abrindo)
     */
    fun triggerSGWUnlocked() {
        playSound(SoundType.SGW_UNLOCK, HapticType.SUCCESS_PATTERN)
    }
    
    /**
     * Gatilho para scan concluído com sucesso
     * Som limpo e satisfatório
     */
    fun triggerScanComplete() {
        playSound(SoundType.SCAN_COMPLETE, HapticType.SHORT_PULSE)
    }
    
    /**
     * Executa padrão de vibração
     */
    fun vibrate(hapticType: HapticType) {
        if (!vibrator.hasVibrator()) return
        
        val effect = when (hapticType) {
            HapticType.SHORT_PULSE -> {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                    VibrationEffect.createPredefined(VibrationEffect.EFFECT_CLICK)
                } else {
                    VibrationEffect.createOneShot(50, VibrationEffect.DEFAULT_AMPLITUDE)
                }
            }
            HapticType.DOUBLE_PULSE -> {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                    VibrationEffect.createPredefined(VibrationEffect.EFFECT_DOUBLE_CLICK)
                } else {
                    val pattern = longArrayOf(0, 50, 100, 50)
                    VibrationEffect.createWaveform(pattern, -1)
                }
            }
            HapticType.LONG_PULSE -> {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                    VibrationEffect.createPredefined(VibrationEffect.EFFECT_HEAVY_CLICK)
                } else {
                    VibrationEffect.createOneShot(200, VibrationEffect.DEFAULT_AMPLITUDE)
                }
            }
            HapticType.SUCCESS_PATTERN -> {
                val pattern = longArrayOf(0, 50, 100, 50, 100, 150)
                VibrationEffect.createWaveform(pattern, -1)
            }
            HapticType.ERROR_PATTERN -> {
                val pattern = longArrayOf(0, 100, 50, 100, 50, 200)
                VibrationEffect.createWaveform(pattern, -1)
            }
            HapticType.TICK -> {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                    VibrationEffect.createPredefined(VibrationEffect.EFFECT_TICK)
                } else {
                    VibrationEffect.createOneShot(20, VibrationEffect.DEFAULT_AMPLITUDE)
                }
            }
        }
        
        vibrator.vibrate(effect)
    }
    
    /**
     * Executa sequência completa de diagnóstico
     * Exemplo de uso combinado
     */
    fun playDiagnosticSequence(faultCount: Int, hasCriticalFault: Boolean) {
        scope.launch {
            // Início do scan
            vibrate(HapticType.TICK)
            delay(100)
            
            // Scan em andamento
            for (i in 1..3) {
                vibrate(HapticType.TICK)
                delay(200)
            }
            
            // Se encontrou falha crítica
            if (hasCriticalFault) {
                triggerCriticalFault()
                delay(500)
            }
            
            // Finaliza com scan completo
            triggerScanComplete()
        }
    }
    
    /**
     * Reproduz áudio longo (ex: instrução em áudio)
     */
    fun playAudioInstruction(resourceId: Int) {
        scope.launch {
            try {
                mediaPlayer?.release()
                mediaPlayer = MediaPlayer.create(context, resourceId)
                mediaPlayer?.isLooping = false
                mediaPlayer?.start()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }
    
    /**
     * Para todos os sons
     */
    fun stopAllSounds() {
        soundPool.autoPause()
        mediaPlayer?.stop()
        mediaPlayer?.release()
        mediaPlayer = null
    }
    
    /**
     * Cancela vibração
     */
    fun cancelVibration() {
        vibrator.cancel()
    }
    
    /**
     * Libera recursos
     */
    fun release() {
        scope.cancel()
        stopAllSounds()
        soundPool.release()
        mediaPlayer?.release()
        mediaPlayer = null
    }
}
