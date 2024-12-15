$(document).ready(function() {
    const debounce = (func, delay) => {
        let debounceTimer;
        return function() {
            const context = this;
            const args = arguments;
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(() => func.apply(context, args), delay);
        };
    };

    $('#search-button').on('click', performSearch);
    $('#search-input').on('input', debounce(handleInput, 300));

    $(document).on('click', '#suggestions-box li', function() {
        const pathwayName = $(this).find('strong').text();
        $('#search-input').val(pathwayName);
        $('#suggestions-box').hide();
        performSearch();
    });

    // Hide suggestions when clicking outside
    $(document).on('click', function(event) {
        if (!$(event.target).closest('#search-section').length) {
            $('#suggestions-box').hide();
        }
    });

    // Handle Enter key for search
    $('#search-input').on('keypress', function(e) {
        if (e.which === 13) { // Enter key
            performSearch();
        }
    });

    function performSearch() {
        const keyword = $('#search-input').val().trim();
        if (!keyword) {
            $('#results-container').html('<p class="error-message">Please enter a search term.</p>');
            return;
        }

        $('#results-container').html('<p class="loading-message">Loading results...</p>');
        $('#suggestions-box').hide();

        $.ajax({
            url: 'search_pathways.cgi', // Ensure this path is correct
            method: 'GET',
            data: { action: 'search', keyword: keyword },
            dataType: 'json',
            success: function(data) {
                console.log('Search Results:', data); // Debugging Line
                displayResults(data);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                $('#results-container').html(`<p class="error-message">Error loading results: ${textStatus}</p>`);
                console.error('AJAX Error:', textStatus, errorThrown);
            }
        });
    }

    function handleInput() {
        const keyword = $(this).val().trim();
        if (keyword.length > 0) {
            $('#suggestions-box').html('<p class="loading-message">Loading suggestions...</p>').show();
            $.ajax({
                url: 'search_pathways.cgi', // Ensure this path is correct
                method: 'GET',
                data: { action: 'suggest', keyword: keyword },
                dataType: 'json',
                success: function(data) {
                    console.log('Display Suggestions Data:', data); // Debugging Line
                    displaySuggestions(data);
                },
                error: function() {
                    $('#suggestions-box').hide();
                }
            });
        } else {
            $('#suggestions-box').hide();
        }
    }

    function displaySuggestions(data) {
        console.log('Display Suggestions Data:', data);
        if (!Array.isArray(data) || data.length === 0) {
            $('#suggestions-box').hide();
            return;
        }

        const suggestions = data.map(item => `
            <li tabindex="0">
                <strong>${escapeHtml(item.pathway_name)}</strong>
                <span class="pathway-class">${escapeHtml(item.class)}</span>
            </li>
        `).join('');
        $('#suggestions-box').html(`<ul>${suggestions}</ul>`).show();
    }

    function displayResults(data) {
        console.log('Display Results Data:', data);
        if (!Array.isArray(data) || data.length === 0) {
            $('#results-container').html('<p class="no-results-message">No results found.</p>');
            return;
        }

        const results = data.map(item => {
            const pathwayName = escapeHtml(item.pathway_name || 'No Name');
            const pathwayClass = escapeHtml(item.class || 'Unclassified');
            const description = escapeHtml(item.description || 'No description available.');

            return `
                <li>
                    <strong>${pathwayName}</strong>
                    <span class="pathway-class">Class: ${pathwayClass}</span>
                    <p>${description}</p>
                    <a href="#" class="details-button"><i class="fas fa-info-circle"></i> Details</a>
                </li>
            `;
        }).join('');
        $('#results-container').html(`<ul>${results}</ul>`);
    }

    function escapeHtml(str) {
        return String(str)
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
});
