from django.http import HttpResponse
from PIL import Image, ImageDraw
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse


def hello(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'hello.html', context)


def generate_image(request):
    colors = [["white", "grey", "darkgrey"],
              ["blue", "lightblue", "darkblue"],
              ["green", "lightgreen", "darkgreen"]]
    [c1, p1, n1, c2, p2, n2] = request.session.get('msg', None)

    k = n1  # Number of rectangles in a row
    rectangle_width = 70  # Width of each rectangle
    rectangle_height = 70  # Height of each rectangle
    margin = 30
    radius = 20

    image1 = Image.new('RGB', (450, 900), colors[c1][1])
    draw1 = ImageDraw.Draw(image1)

    rows = (k - 1) // 4

    # Draw 'k' rectangles in rows of 4 below the existing rectangle
    for row in range(rows + 1):
        fill_color = colors[c1][0]
        for col in range(4):
            if row * 4 + col < k:
                x0 = col * (rectangle_width + margin) + 50
                y0 = row * (rectangle_height + margin) + 100
                x1 = x0 + rectangle_width
                y1 = y0 + rectangle_height
                draw1.rounded_rectangle((x0, y0, x1, y1), radius=radius, fill=fill_color)
        if row == rows and p1 == 1:
            y = 100 + row * (rectangle_height + margin)
            draw1.rounded_rectangle((100, y, 800, y + 100), radius=radius, fill=fill_color)

    image2 = Image.new('RGB', (480, 900), colors[c2][1])
    draw2 = ImageDraw.Draw(image2)

    rows = (k - 1) // 4

    # Draw 'k' rectangles in rows of 4 below the existing rectangle
    for row in range(rows + 1):
        fill_color = colors[c2][0]
        for col in range(4):
            if row * 4 + col < k:
                x0 = col * (rectangle_width + margin) + 50
                y0 = row * (rectangle_height + margin) + 100
                x1 = x0 + rectangle_width
                y1 = y0 + rectangle_height
                draw2.rounded_rectangle((x0, y0, x1, y1), radius=radius, fill=fill_color)
        if row == rows and p2 == 1:
            y = 100 + (row + 1) * (rectangle_height + margin)
            draw2.rounded_rectangle((50, y, 430, y + 100), radius=radius, fill=fill_color)

    combined_width = image1.width + margin + image2.width
    combined_image = Image.new('RGB', (combined_width, 800), 'white')
    combined_image.paste(image1, (0, 0))
    combined_image.paste(image2, (image1.width + margin, 0))

    # Save the combined image as JPEG
    response = HttpResponse(content_type='image/jpeg')
    combined_image.save(response, 'JPEG')

    return response


def process_integers(request):
    if request.method == 'POST':
        c1 = int(request.POST['color1'])
        p1 = int(request.POST['pattern1'])
        n1 = int(request.POST['number1'])
        c2 = int(request.POST['color2'])
        p2 = int(request.POST['pattern2'])
        n2 = int(request.POST['number2'])

        request.session['msg'] = [c1, p1, n1, c2, p2, n2]

        return HttpResponseRedirect("image/")

    return render(request, 'hello.html')
