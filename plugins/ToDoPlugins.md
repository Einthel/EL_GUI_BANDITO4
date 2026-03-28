## Tune Plugin Optimization Plan

### 1. TuneBanditoPlugin (Server)
- [ ] **Refactor `handle_button_press`**:
    - Remove duplicate logic for `sound_volume_slider` and `mic_volume_slider`.
    - Create a unified handler for volume changes (e.g., `_handle_volume_slider_input(slider_id, value)`).
    - Simplify the ID/payload parsing logic (the "hack" for `id|value` parsing can be cleaner).
- [ ] **Refactor `_set_volume_from_client`**:
    - Merge the `if dev_type == "sound"` and `elif dev_type == "mic"` blocks into a single flow using a mapping dictionary for device keys and config keys.
    - Reduce code duplication for device lookup and volume setting.
- [ ] **Cleanup**:
    - Remove excessive debug `print` statements (e.g., `[Tn] handle_button_press...`) once stable.

### 2. TnAudioManager
- [ ] **Optimize `AudioStatusListener`**:
    - Consider keeping the COM context initialized if the polling interval is very short (though current `CoInitialize` per loop is safer for threading).
    - Review `set_mute_mic`/`set_mute_sound` wrappers; they are identical to `_set_device_mute`. Consider deprecating them or keeping them strictly as aliases for API clarity.

### 3. TuneClientoPlugin (Client)
- [ ] **Event Handling**:
    - Review usage of `sliderReleased`. While it reduces network traffic, `valueChanged` with a debouncer (e.g., sending update only after 100-200ms of inactivity) would provide a smoother real-time experience for the user.
- [ ] **Cleanup**:
    - Remove debug prints like `[Tn] Client sending sound volume...`.

### 4. General
- [ ] **Protocol**:
    - Document the "composite ID" protocol (`id|value`) used for sliders in a developer note or README, as it's a workaround for Core's payload limitations.
