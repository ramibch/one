from django.db.models import TextChoices


class AnimationType(TextChoices):
    VANILLA = "vanilla", "Vanilla"
    ON_MOUSE_OVER = "onmouseover", "On event: onmouseover"


class AnimationDelay(TextChoices):
    TWO = "2s", "2 Seconds"
    THREE = "3s", "3 Seconds"
    FOUR = "4s", "4 Seconds"
    FIVE = "5s", "5 Seconds"


class AnimationSpeed(TextChoices):
    SLOW = "slow", "Slow 2s"
    SLOWER = "slower", "Slow 3s"
    FAST = "fast", "Fast 800ms"
    FASTER = "faster", "Faster 500ms"


class AnimationRepeat(TextChoices):
    ONE = "repeat-1", "1 Time"
    TWO = "repeat-2", "2 Times"
    THREE = "repeat-3", "3 Times"
    INFINITE = "infinite", "Infinite times"


class AttentionSeekers(TextChoices):
    BOUNCE = "bounce", "Bounce"
    FLASH = "flash", "Flash"
    PULSE = "pulse", "Pulse"
    RUBBER_BAND = "rubberBand", "Rubber Band"
    SHAKE_X = "shakeX", "Shake X"
    SHAKE_Y = "shakeY", "Shake Y"
    HEAD_SHAKE = "headShake", "Head Shake"
    SWING = "swing", "Swing"
    TADA = "tada", "Tada"
    WOBBLE = "wobble", "Wobble"
    JELLO = "jello", "Jello"
    HEART_BEAT = "heartBeat", "Heart Beat"


class BackEntrances(TextChoices):
    BACK_IN_DOWN = "backInDown", "Back In Down"
    BACK_IN_LEFT = "backInLeft", "Back In Left"
    BACK_IN_RIGHT = "backInRight", "Back In Right"
    BACK_IN_UP = "backInUp", "Back In Up"


class BackExits(TextChoices):
    BACK_OUT_DOWN = "backOutDown", "Back Out Down"
    BACK_OUT_LEFT = "backOutLeft", "Back Out Left"
    BACK_OUT_RIGHT = "backOutRight", "Back Out Right"
    BACK_OUT_UP = "backOutUp", "Back Out Up"


class BouncingEntrances(TextChoices):
    BOUNCE_IN = "bounceIn", "Bounce In"
    BOUNCE_IN_DOWN = "bounceInDown", "Bounce In Down"
    BOUNCE_IN_LEFT = "bounceInLeft", "Bounce In Left"
    BOUNCE_IN_RIGHT = "bounceInRight", "Bounce In Right"
    BOUNCE_IN_UP = "bounceInUp", "Bounce In Up"


class BouncingExits(TextChoices):
    BOUNCE_OUT = "bounceOut", "Bounce Out"
    BOUNCE_OUT_DOWN = "bounceOutDown", "Bounce Out Down"
    BOUNCE_OUT_LEFT = "bounceOutLeft", "Bounce Out Left"
    BOUNCE_OUT_RIGHT = "bounceOutRight", "Bounce Out Right"
    BOUNCE_OUT_UP = "bounceOutUp", "Bounce Out Up"


class FadingEntrances(TextChoices):
    FADE_IN = "fadeIn", "Fade In"
    FADE_IN_DOWN = "fadeInDown", "Fade In Down"
    FADE_IN_DOWN_BIG = "fadeInDownBig", "Fade In Down Big"
    FADE_IN_LEFT = "fadeInLeft", "Fade In Left"
    FADE_IN_LEFT_BIG = "fadeInLeftBig", "Fade In Left Big"
    FADE_IN_RIGHT = "fadeInRight", "Fade In Right"
    FADE_IN_RIGHT_BIG = "fadeInRightBig", "Fade In Right Big"
    FADE_IN_UP = "fadeInUp", "Fade In Up"
    FADE_IN_UP_BIG = "fadeInUpBig", "Fade In Up Big"
    FADE_IN_TOP_LEFT = "fadeInTopLeft", "Fade In Top Left"
    FADE_IN_TOP_RIGHT = "fadeInTopRight", "Fade In Top Right"
    FADE_IN_BOTTOM_LEFT = "fadeInBottomLeft", "Fade In Bottom Left"
    FADE_IN_BOTTOM_RIGHT = "fadeInBottomRight", "Fade In Bottom Right"


class FadingExits(TextChoices):
    FADE_OUT = "fadeOut", "Fade Out"
    FADE_OUT_DOWN = "fadeOutDown", "Fade Out Down"
    FADE_OUT_DOWN_BIG = "fadeOutDownBig", "Fade Out Down Big"
    FADE_OUT_LEFT = "fadeOutLeft", "Fade Out Left"
    FADE_OUT_LEFT_BIG = "fadeOutLeftBig", "Fade Out Left Big"
    FADE_OUT_RIGHT = "fadeOutRight", "Fade Out Right"
    FADE_OUT_RIGHT_BIG = "fadeOutRightBig", "Fade Out Right Big"
    FADE_OUT_UP = "fadeOutUp", "Fade Out Up"
    FADE_OUT_UP_BIG = "fadeOutUpBig", "Fade Out Up Big"
    FADE_OUT_TOP_LEFT = "fadeOutTopLeft", "Fade Out Top Left"
    FADE_OUT_TOP_RIGHT = "fadeOutTopRight", "Fade Out Top Right"
    FADE_OUT_BOTTOM_RIGHT = "fadeOutBottomRight", "Fade Out Bottom Right"
    FADE_OUT_BOTTOM_LEFT = "fadeOutBottomLeft", "Fade Out Bottom Left"


class Flippers(TextChoices):
    FLIP = "flip", "Flip"
    FLIP_IN_X = "flipInX", "Flip In X"
    FLIP_IN_Y = "flipInY", "Flip In Y"
    FLIP_OUT_X = "flipOutX", "Flip Out X"
    FLIP_OUT_Y = "flipOutY", "Flip Out Y"


class Lightspeed(TextChoices):
    LIGHT_SPEED_IN_RIGHT = "lightSpeedInRight", "Light Speed In Right"
    LIGHT_SPEED_IN_LEFT = "lightSpeedInLeft", "Light Speed In Left"
    LIGHT_SPEED_OUT_RIGHT = "lightSpeedOutRight", "Light Speed Out Right"
    LIGHT_SPEED_OUT_LEFT = "lightSpeedOutLeft", "Light Speed Out Left"


class RotatingEntrances(TextChoices):
    ROTATE_IN = "rotateIn", "Rotate In"
    ROTATE_IN_DOWN_LEFT = "rotateInDownLeft", "Rotate In Down Left"
    ROTATE_IN_DOWN_RIGHT = "rotateInDownRight", "Rotate In Down Right"
    ROTATE_IN_UP_LEFT = "rotateInUpLeft", "Rotate In Up Left"
    ROTATE_IN_UP_RIGHT = "rotateInUpRight", "Rotate In Up Right"


class RotatingExits(TextChoices):
    ROTATE_OUT = "rotateOut", "Rotate Out"
    ROTATE_OUT_DOWN_LEFT = "rotateOutDownLeft", "Rotate Out Down Left"
    ROTATE_OUT_DOWN_RIGHT = "rotateOutDownRight", "Rotate Out Down Right"
    ROTATE_OUT_UP_LEFT = "rotateOutUpLeft", "Rotate Out Up Left"
    ROTATE_OUT_UP_RIGHT = "rotateOutUpRight", "Rotate Out Up Right"


class Specials(TextChoices):
    HINGE = "hinge", "Hinge"
    JACK_IN_THE_BOX = "jackInTheBox", "Jack in the Box"
    ROLL_IN = "rollIn", "Roll In"
    ROLL_OUT = "rollOut", "Roll Out"


class ZoomingEntrances(TextChoices):
    ZOOM_IN = "zoomIn", "Zoom In"
    ZOOM_IN_DOWN = "zoomInDown", "Zoom In Down"
    ZOOM_IN_LEFT = "zoomInLeft", "Zoom In Left"
    ZOOM_IN_RIGHT = "zoomInRight", "Zoom In Right"
    ZOOM_IN_UP = "zoomInUp", "Zoom In Up"


class ZoomingExits(TextChoices):
    ZOOM_OUT = "zoomOut", "zoomOut"
    ZOOM_OUT_DOWN = "zoomOutDown", "zoomOutDown"
    ZOOM_OUT_LEFT = "zoomOutLeft", "zoomOutLeft"
    ZOOM_OUT_RIGHT = "zoomOutRight", "zoomOutRight"
    ZOOM_OUT_UP = "zoomOutUp", "zoomOutUp"


class SlidingEntrances(TextChoices):
    SLIDE_IN_UP = "slideInUp", "slideInUp"
    SLIDE_IN_DOWN = "slideInDown", "slideInDown"
    SLIDE_IN_LEFT = "slideInLeft", "slideInLeft"
    SLIDE_IN_RIGHT = "slideInRight", "slideInRight"


class SlidingExits(TextChoices):
    SLIDE_OUT_DOWN = "slideOutDown", "slideOutDown"
    SLIDE_OUT_LEFT = "slideOutLeft", "slideOutLeft"
    SLIDE_OUT_RIGHT = "slideOutRight", "slideOutRight"
    SLIDE_OUT_UP = "slideOutUp", "slideOutUp"
