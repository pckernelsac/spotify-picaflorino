/**
 * Reproductor de Audio Avanzado para Spotify Picaflorino
 * I.E. 30012 Victor Alberto Gill Mallma
 */

class AudioPlayer {
    constructor() {
        this.audio = new Audio();
        this.currentSong = null;
        this.playlist = [];
        this.currentIndex = 0;
        this.isPlaying = false;
        this.isShuffle = false;
        this.isRepeat = false;
        this.volume = 0.8;
        
        this.setupEventListeners();
        this.initializeUI();
        this.audio.volume = this.volume;
    }
    
    setupEventListeners() {
        // Eventos del audio
        this.audio.addEventListener('loadstart', () => this.showLoading());
        this.audio.addEventListener('loadeddata', () => this.hideLoading());
        this.audio.addEventListener('canplay', () => this.updatePlayButton());
        this.audio.addEventListener('play', () => this.onPlay());
        this.audio.addEventListener('pause', () => this.onPause());
        this.audio.addEventListener('ended', () => this.onSongEnd());
        this.audio.addEventListener('timeupdate', () => this.updateProgress());
        this.audio.addEventListener('error', (e) => this.onError(e));
        
        // Controles de teclado
        document.addEventListener('keydown', (e) => this.handleKeyPress(e));
        
        // Controles de la UI
        this.setupUIControls();
    }
    
    initializeUI() {
        // Crear elementos de la UI si no existen
        this.createPlayerElements();
        this.updateVolumeSlider();
    }
    
    createPlayerElements() {
        const playerContainer = document.getElementById('audio-player-container');
        if (!playerContainer) return;
        
        playerContainer.innerHTML = `
            <div class="audio-player bg-gray-900 text-white p-4 rounded-lg shadow-lg">
                <!-- Información de la canción -->
                <div class="song-info flex items-center mb-4">
                    <div class="cover-image w-16 h-16 bg-gray-700 rounded-lg mr-4 flex items-center justify-center">
                        <i class="fas fa-music text-gray-400 text-2xl" id="default-cover"></i>
                        <img id="song-cover" class="w-full h-full object-cover rounded-lg hidden" alt="Portada">
                    </div>
                    <div class="song-details flex-1">
                        <h3 id="song-title" class="text-lg font-semibold">Selecciona una canción</h3>
                        <p id="song-artist" class="text-gray-400">Artista</p>
                        <p id="song-album" class="text-gray-500 text-sm">Álbum</p>
                    </div>
                    <div class="loading hidden" id="loading-indicator">
                        <i class="fas fa-spinner fa-spin text-spotify-green"></i>
                    </div>
                </div>
                
                <!-- Barra de progreso -->
                <div class="progress-container mb-4">
                    <div class="flex justify-between text-sm text-gray-400 mb-2">
                        <span id="current-time">0:00</span>
                        <span id="total-time">0:00</span>
                    </div>
                    <div class="progress-bar-container bg-gray-700 h-2 rounded-full cursor-pointer" id="progress-container">
                        <div class="progress-bar bg-spotify-green h-2 rounded-full transition-all duration-300" id="progress-bar" style="width: 0%"></div>
                    </div>
                </div>
                
                <!-- Controles principales -->
                <div class="controls flex items-center justify-center space-x-6 mb-4">
                    <button id="shuffle-btn" class="control-btn text-gray-400 hover:text-white transition-colors duration-200">
                        <i class="fas fa-random text-lg"></i>
                    </button>
                    
                    <button id="prev-btn" class="control-btn text-gray-400 hover:text-white transition-colors duration-200">
                        <i class="fas fa-step-backward text-xl"></i>
                    </button>
                    
                    <button id="play-pause-btn" class="play-btn bg-spotify-green hover:bg-green-600 text-white w-12 h-12 rounded-full flex items-center justify-center transition-all duration-200 transform hover:scale-105">
                        <i class="fas fa-play text-lg" id="play-icon"></i>
                    </button>
                    
                    <button id="next-btn" class="control-btn text-gray-400 hover:text-white transition-colors duration-200">
                        <i class="fas fa-step-forward text-xl"></i>
                    </button>
                    
                    <button id="repeat-btn" class="control-btn text-gray-400 hover:text-white transition-colors duration-200">
                        <i class="fas fa-redo text-lg"></i>
                    </button>
                </div>
                
                <!-- Controles de volumen -->
                <div class="volume-controls flex items-center space-x-3">
                    <button id="mute-btn" class="text-gray-400 hover:text-white transition-colors duration-200">
                        <i class="fas fa-volume-up" id="volume-icon"></i>
                    </button>
                    <div class="volume-slider-container flex-1">
                        <input type="range" id="volume-slider" class="volume-slider w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer" 
                               min="0" max="100" value="80">
                    </div>
                    <span id="volume-percentage" class="text-sm text-gray-400 w-10">80%</span>
                </div>
                
                <!-- Ecualizador visual (opcional) -->
                <div class="equalizer hidden mt-4" id="equalizer">
                    <div class="eq-bars flex items-end justify-center space-x-1 h-8">
                        ${Array.from({length: 10}, (_, i) => 
                            `<div class="eq-bar bg-spotify-green w-2 music-wave" style="height: ${Math.random() * 100}%; animation-delay: ${i * 0.1}s;"></div>`
                        ).join('')}
                    </div>
                </div>
            </div>
        `;
    }
    
    setupUIControls() {
        // Play/Pause
        const playPauseBtn = document.getElementById('play-pause-btn');
        if (playPauseBtn) {
            playPauseBtn.addEventListener('click', () => this.togglePlayPause());
        }
        
        // Anterior/Siguiente
        const prevBtn = document.getElementById('prev-btn');
        const nextBtn = document.getElementById('next-btn');
        if (prevBtn) prevBtn.addEventListener('click', () => this.playPrevious());
        if (nextBtn) nextBtn.addEventListener('click', () => this.playNext());
        
        // Shuffle/Repeat
        const shuffleBtn = document.getElementById('shuffle-btn');
        const repeatBtn = document.getElementById('repeat-btn');
        if (shuffleBtn) shuffleBtn.addEventListener('click', () => this.toggleShuffle());
        if (repeatBtn) repeatBtn.addEventListener('click', () => this.toggleRepeat());
        
        // Volumen
        const volumeSlider = document.getElementById('volume-slider');
        const muteBtn = document.getElementById('mute-btn');
        if (volumeSlider) {
            volumeSlider.addEventListener('input', (e) => this.setVolume(e.target.value / 100));
        }
        if (muteBtn) muteBtn.addEventListener('click', () => this.toggleMute());
        
        // Barra de progreso
        const progressContainer = document.getElementById('progress-container');
        if (progressContainer) {
            progressContainer.addEventListener('click', (e) => this.seekTo(e));
        }
    }
    
    loadSong(songId) {
        this.showLoading();
        
        fetch(`/api/cancion/${songId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Canción no encontrada');
                }
                return response.json();
            })
            .then(song => {
                this.currentSong = song;
                this.audio.src = song.archivo;
                this.updateSongInfo(song);
                
                // Registrar reproducción
                this.registerPlayback(songId);
            })
            .catch(error => {
                console.error('Error al cargar canción:', error);
                this.showError('Error al cargar la canción');
            })
            .finally(() => {
                this.hideLoading();
            });
    }
    
    loadPlaylist(songs, startIndex = 0) {
        this.playlist = songs;
        this.currentIndex = startIndex;
        
        if (this.playlist.length > 0) {
            this.loadSong(this.playlist[this.currentIndex].id);
        }
    }
    
    updateSongInfo(song) {
        const titleEl = document.getElementById('song-title');
        const artistEl = document.getElementById('song-artist');
        const albumEl = document.getElementById('song-album');
        const coverEl = document.getElementById('song-cover');
        const defaultCoverEl = document.getElementById('default-cover');
        
        if (titleEl) titleEl.textContent = song.titulo;
        if (artistEl) artistEl.textContent = song.artista;
        if (albumEl) albumEl.textContent = song.album || 'Álbum desconocido';
        
        if (coverEl && defaultCoverEl) {
            if (song.cover) {
                coverEl.src = song.cover;
                coverEl.classList.remove('hidden');
                defaultCoverEl.classList.add('hidden');
            } else {
                coverEl.classList.add('hidden');
                defaultCoverEl.classList.remove('hidden');
            }
        }
        
        // Actualizar título de la página
        document.title = `${song.titulo} - ${song.artista} | Spotify Picaflorino`;
    }
    
    togglePlayPause() {
        if (this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }
    
    play() {
        if (this.audio.src) {
            this.audio.play()
                .then(() => {
                    this.isPlaying = true;
                    this.updatePlayButton();
                    this.showEqualizer();
                })
                .catch(error => {
                    console.error('Error al reproducir:', error);
                    this.showError('Error al reproducir la canción');
                });
        }
    }
    
    pause() {
        this.audio.pause();
        this.isPlaying = false;
        this.updatePlayButton();
        this.hideEqualizer();
    }
    
    stop() {
        this.audio.pause();
        this.audio.currentTime = 0;
        this.isPlaying = false;
        this.updatePlayButton();
        this.hideEqualizer();
    }
    
    playNext() {
        if (this.playlist.length === 0) return;
        
        if (this.isShuffle) {
            this.currentIndex = Math.floor(Math.random() * this.playlist.length);
        } else {
            this.currentIndex = (this.currentIndex + 1) % this.playlist.length;
        }
        
        this.loadSong(this.playlist[this.currentIndex].id);
    }
    
    playPrevious() {
        if (this.playlist.length === 0) return;
        
        if (this.audio.currentTime > 3) {
            // Si han pasado más de 3 segundos, reiniciar la canción actual
            this.audio.currentTime = 0;
        } else {
            // Ir a la canción anterior
            this.currentIndex = this.currentIndex === 0 ? 
                this.playlist.length - 1 : this.currentIndex - 1;
            this.loadSong(this.playlist[this.currentIndex].id);
        }
    }
    
    setVolume(volume) {
        this.volume = Math.max(0, Math.min(1, volume));
        this.audio.volume = this.volume;
        this.updateVolumeSlider();
        this.updateVolumeIcon();
    }
    
    toggleMute() {
        if (this.audio.volume > 0) {
            this.audio.volume = 0;
        } else {
            this.audio.volume = this.volume;
        }
        this.updateVolumeSlider();
        this.updateVolumeIcon();
    }
    
    toggleShuffle() {
        this.isShuffle = !this.isShuffle;
        const shuffleBtn = document.getElementById('shuffle-btn');
        if (shuffleBtn) {
            shuffleBtn.classList.toggle('text-spotify-green', this.isShuffle);
            shuffleBtn.classList.toggle('text-gray-400', !this.isShuffle);
        }
    }
    
    toggleRepeat() {
        this.isRepeat = !this.isRepeat;
        const repeatBtn = document.getElementById('repeat-btn');
        if (repeatBtn) {
            repeatBtn.classList.toggle('text-spotify-green', this.isRepeat);
            repeatBtn.classList.toggle('text-gray-400', !this.isRepeat);
        }
    }
    
    seekTo(event) {
        const progressContainer = event.currentTarget;
        const rect = progressContainer.getBoundingClientRect();
        const clickX = event.clientX - rect.left;
        const width = rect.width;
        const percentage = clickX / width;
        
        if (this.audio.duration) {
            this.audio.currentTime = this.audio.duration * percentage;
        }
    }
    
    updateProgress() {
        if (!this.audio.duration) return;
        
        const progress = (this.audio.currentTime / this.audio.duration) * 100;
        const progressBar = document.getElementById('progress-bar');
        const currentTimeEl = document.getElementById('current-time');
        const totalTimeEl = document.getElementById('total-time');
        
        if (progressBar) {
            progressBar.style.width = `${progress}%`;
        }
        
        if (currentTimeEl) {
            currentTimeEl.textContent = this.formatTime(this.audio.currentTime);
        }
        
        if (totalTimeEl) {
            totalTimeEl.textContent = this.formatTime(this.audio.duration);
        }
    }
    
    updatePlayButton() {
        const playIcon = document.getElementById('play-icon');
        if (playIcon) {
            playIcon.className = this.isPlaying ? 'fas fa-pause text-lg' : 'fas fa-play text-lg';
        }
    }
    
    updateVolumeSlider() {
        const volumeSlider = document.getElementById('volume-slider');
        const volumePercentage = document.getElementById('volume-percentage');
        
        if (volumeSlider) {
            volumeSlider.value = this.audio.volume * 100;
        }
        
        if (volumePercentage) {
            volumePercentage.textContent = `${Math.round(this.audio.volume * 100)}%`;
        }
    }
    
    updateVolumeIcon() {
        const volumeIcon = document.getElementById('volume-icon');
        if (!volumeIcon) return;
        
        if (this.audio.volume === 0) {
            volumeIcon.className = 'fas fa-volume-mute';
        } else if (this.audio.volume < 0.5) {
            volumeIcon.className = 'fas fa-volume-down';
        } else {
            volumeIcon.className = 'fas fa-volume-up';
        }
    }
    
    showLoading() {
        const loadingIndicator = document.getElementById('loading-indicator');
        if (loadingIndicator) {
            loadingIndicator.classList.remove('hidden');
        }
    }
    
    hideLoading() {
        const loadingIndicator = document.getElementById('loading-indicator');
        if (loadingIndicator) {
            loadingIndicator.classList.add('hidden');
        }
    }
    
    showEqualizer() {
        const equalizer = document.getElementById('equalizer');
        if (equalizer) {
            equalizer.classList.remove('hidden');
        }
    }
    
    hideEqualizer() {
        const equalizer = document.getElementById('equalizer');
        if (equalizer) {
            equalizer.classList.add('hidden');
        }
    }
    
    showError(message) {
        // Crear notificación de error
        const errorDiv = document.createElement('div');
        errorDiv.className = 'fixed top-4 right-4 bg-red-500 text-white px-4 py-2 rounded-lg shadow-lg z-50';
        errorDiv.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-exclamation-triangle mr-2"></i>
                <span>${message}</span>
                <button class="ml-2" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;
        
        document.body.appendChild(errorDiv);
        
        // Auto-remove después de 5 segundos
        setTimeout(() => {
            if (errorDiv.parentElement) {
                errorDiv.remove();
            }
        }, 5000);
    }
    
    registerPlayback(songId) {
        // Registrar la reproducción en el servidor
        fetch('/api/reproduccion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            },
            body: JSON.stringify({
                cancion_id: songId,
                timestamp: Date.now()
            })
        }).catch(error => {
            console.error('Error al registrar reproducción:', error);
        });
    }
    
    getCSRFToken() {
        const token = document.querySelector('meta[name=csrf-token]');
        return token ? token.getAttribute('content') : '';
    }
    
    formatTime(seconds) {
        if (!seconds || isNaN(seconds)) return '0:00';
        
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs.toString().padStart(2, '0')}`;
    }
    
    handleKeyPress(event) {
        // Solo manejar teclas si no estamos en un input
        if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
            return;
        }
        
        switch (event.code) {
            case 'Space':
                event.preventDefault();
                this.togglePlayPause();
                break;
            case 'ArrowRight':
                event.preventDefault();
                this.playNext();
                break;
            case 'ArrowLeft':
                event.preventDefault();
                this.playPrevious();
                break;
            case 'ArrowUp':
                event.preventDefault();
                this.setVolume(Math.min(1, this.volume + 0.1));
                break;
            case 'ArrowDown':
                event.preventDefault();
                this.setVolume(Math.max(0, this.volume - 0.1));
                break;
        }
    }
    
    // Event handlers
    onPlay() {
        this.isPlaying = true;
        this.updatePlayButton();
        this.showEqualizer();
    }
    
    onPause() {
        this.isPlaying = false;
        this.updatePlayButton();
        this.hideEqualizer();
    }
    
    onSongEnd() {
        if (this.isRepeat) {
            this.audio.currentTime = 0;
            this.play();
        } else {
            this.playNext();
        }
    }
    
    onError(event) {
        console.error('Error en el reproductor:', event);
        this.showError('Error al cargar el archivo de audio');
        this.isPlaying = false;
        this.updatePlayButton();
    }
    
    // Destructor
    destroy() {
        this.audio.pause();
        this.audio.src = '';
        document.removeEventListener('keydown', this.handleKeyPress);
    }
}

// Función para inicializar el reproductor globalmente
function initializePlayer() {
    if (typeof window.audioPlayer !== 'undefined') {
        window.audioPlayer.destroy();
    }
    
    window.audioPlayer = new AudioPlayer();
}

// Funciones auxiliares para usar desde templates
function playTSong(songId) {
    if (window.audioPlayer) {
        window.audioPlayer.loadSong(songId);
    }
}

function playPlaylist(songs, startIndex = 0) {
    if (window.audioPlayer) {
        window.audioPlayer.loadPlaylist(songs, startIndex);
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Solo inicializar si hay un contenedor del reproductor
    if (document.getElementById('audio-player-container')) {
        initializePlayer();
    }
});

// Limpiar cuando se sale de la página
window.addEventListener('beforeunload', function() {
    if (window.audioPlayer) {
        window.audioPlayer.destroy();
    }
});
