
// Delete Pokedex
$('#deletePokedex').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget);
    var pokedexSlug = button.data('pokedex-slug');
    var formAction = deletePokedexBaseUrl.replace('placeholder-slug', pokedexSlug);
    $('#deletePokedexForm').attr('action', formAction);
});

// Color picker for Pokedex
const pickr = Pickr.create({
    el: '.color-picker',
    theme: 'nano',
    useAsButton: true,
    swatches: [
        'rgba(244, 67, 54, 1)',
        'rgba(233, 30, 99, 0.95)',
        'rgba(156, 39, 176, 0.9)',
        'rgba(103, 58, 183, 0.85)',
        'rgba(63, 81, 181, 0.8)',
        'rgba(33, 150, 243, 0.75)',
        'rgba(3, 169, 244, 0.7)',
        'rgba(0, 188, 212, 0.7)',
        'rgba(0, 150, 136, 0.75)',
        'rgba(76, 175, 80, 0.8)',
        'rgba(139, 195, 74, 0.85)',
        'rgba(205, 220, 57, 0.9)',
        'rgba(255, 235, 59, 0.95)',
        'rgba(255, 193, 7, 1)'
    ],

    components: {

        // Main components
        preview: true,
        opacity: true,
        hue: true,

        // Input / output Options
        interaction: {
            hex: true,
            rgba: true,
            hsla: true,
            hsva: true,
            cmyk: true,
            input: true,
            clear: true,
            save: true
        }
    }
});

pickr.on('init', instance => {

    // Grab actual input-element
    const {result} = instance.getRoot().interaction;

    // Listen to any key-events
    result.addEventListener('keydown', e => {

        // Detect whever the user pressed "Enter" on their keyboard
        if (e.key === 'Enter') {
            instance.applyColor(); // Save the currently selected color
            instance.hide(); // Hide modal
        }
    }, {capture: true});
});