import particles, gravity, obstacles, sys, pygame

class ParticleEffect:
	def __init__(self, display, pos, size):
		self.display = display
		self.pos = pos
		self.size = size
		
		self.left = pos[0]
		self.top = pos[1]
		self.right = pos[0] + size[0]
		self.bottom = pos[1] + size[1]
		
		self.particles = []
		self.sources = []
		self.gravities = []
		self.obstacles = []
	
	def Update(self):
		for source in self.sources:
			source.Update()
		
		for gravity in self.gravities:
			gravity.Update()
		
		for obstacle in self.obstacles:
			obstacle.Update()

		for particle in self.particles:
			totalforce = [0.0, 0.0]
			
			for gravity in self.gravities:
				force = gravity.GetForce(particle.pos)
				totalforce[0] += force[0]
				totalforce[1] += force[1]
			
			for obstacle in self.obstacles:
				if (not obstacle.OutOfRange(particle.pos)) and (obstacle.InsideObject(particle.pos)):
					particle.pos = obstacle.GetResolved(particle.pos)
				
				force = obstacle.GetForce(particle.pos, particle.velocity)
				totalforce[0] += force[0]
				totalforce[1] += force[1]
			
			particle.velocity = [particle.velocity[0] + totalforce[0], particle.velocity[1] + totalforce[1]]
			
			particle.Update()
		
		# Delete dead particles
		for particle in self.particles:
			if not particle.alive:
				self.particles.remove(particle)
	
	def Redraw(self):
		for particle in self.particles:
			particle.Draw(self.display)
			
		for obstacle in self.obstacles:
			obstacle.Draw(self.display)
	
	def CreateSource(self, pos = (0, 0), initspeed = 0.0, initdirection = 0.0, initspeedrandrange = 0.0, initdirectionrandrange = 0.0, particlesperframe = 0, particlelife = 0, genspacing = 0, drawtype = 0, colour = (0, 0, 0), radius = 0.0, length = 0.0, image = None):
		newsource = particles.ParticleSource(self, pos, initspeed, initdirection, initspeedrandrange, initdirectionrandrange, particlesperframe, particlelife, genspacing, drawtype, colour, radius, length, image)
		self.sources.append(newsource)
		return newsource  # Effectively a reference
	
	def CreatePointGravity(self, strength = 0.0, strengthrandrange = 0.0, pos = (0, 0)):
		newgrav = gravity.PointGravity(strength, strengthrandrange, pos)
		self.gravities.append(newgrav)
		return newgrav
	
	def CreateDirectedGravity(self, strength = 0.0, strengthrandrange = 0.0, direction = [0, 1]):
		newgrav = gravity.DirectedGravity(strength, strengthrandrange, direction)
		self.gravities.append(newgrav)
		return newgrav
	
	def CreateCircle(self, pos = (0, 0), colour = (0, 0, 0), bounce = 1.0, radius = 0.0):
		newcircle = obstacles.Circle(pos, colour, bounce, radius)
		self.obstacles.append(newcircle)
		return newcircle
	
	def CreateRectangle(self, pos = (0, 0), colour = (0, 0, 0), bounce = 1.0, width = 0.0, height = 0.0):
		newrect = obstacles.Rectangle(pos, colour, bounce, width, height)
		self.obstacles.append(newrect)
		return newrect
	
	def CreateBoundaryLine(self, pos = (0, 0), colour = (0, 0, 0), bounce = 1.0, normal = [0, 1]):
		newline = obstacles.BoundaryLine(pos, colour, bounce, normal)
		self.obstacles.append(newline)
		return newline
	
	def AddParticle(self, particle):
		self.particles.append(particle)

class Option:

	hovered = False

	def __init__(self, text, pos, font=0):
		self.text = text
		self.pos = pos
		if (font != 0):
			self.font = font
		else:
			self.font = menu_font
		self.set_rect()
		self.draw()

	def draw(self):
		self.set_rend()
		screen.blit(self.rend, self.rect)

	def set_rend(self):
		self.rend = self.font.render(self.text, True, self.get_color())

	def get_color(self):
		if self.hovered:
			return (251, 223, 124)
		else:
			return (0, 0, 0)

	def set_rect(self):
		self.set_rend()
		self.rect = self.rend.get_rect()
		self.rect.center = (int((width / 2)), int(height / 2))
		self.rect.top = self.pos


effectTimeTable = ((3300, 4350), (7500, 8500), (11580, 12580), (15500, 16500), (19500, 20500))
effectTimeMin = effectTimeTable[0][0]
effectTimeMax = effectTimeTable[len(effectTimeTable)-1][1]
def isEffect (musicPos):
	if (musicPos < effectTimeMin):
		return False
	if (musicPos > effectTimeMax):
		return True
	for effect in effectTimeTable:
		if (effect[0] <= musicPos <= effect[1]):
			return True
	return False

if __name__ == '__main__':
	size = width, height = 800 , 600
	screen = pygame.display.set_mode(size)
	bg = pygame.image.load("background.jpg")
	bg = pygame.transform.scale(bg, size)
	light = pygame.image.load('circle.png')

	pygame.init()
	menu_font = pygame.font.Font('font.ttf', 30)
	title_font = pygame.font.Font('font.ttf', 80)
	first, space = 250, 50
	options = [
		Option("SCORCHED EARTCH", 20, title_font),
		Option("NEW GAME", (first)),
		Option("OPTIONS", (first + space)),
		Option("EXIT", (first + (space * 2)))
	]

	clock = pygame.time.Clock()
	test = ParticleEffect(screen, (0, 0), (800, 600))
	testgrav = test.CreatePointGravity(strength = -5, pos = (width/2, height/2 + 100))

	testsource = test.CreateSource((-10, -10), initspeed = 5.0, initdirection = 2.35619449, initspeedrandrange = 2.0, initdirectionrandrange = 1.5, particlesperframe = 5, particlelife = 75, drawtype = particles.DRAWTYPE_SCALELINE, colour = (255, 255, 255), length = 10.0)
	testsource.CreateParticleKeyframe(50, colour = (3, 74, 236), length = 10.0)
	testsource.CreateParticleKeyframe(75, colour = (255, 255, 0), length = 10.0)
	testsource.CreateParticleKeyframe(100, colour = (0, 255, 255), length = 10.0)
	testsource.CreateParticleKeyframe(125, colour = (0, 0, 0), length = 10.0)

	testsource = test.CreateSource((width + 10, 0), initspeed = 5.0, initdirection = 4.15619449, initspeedrandrange = 2.0, initdirectionrandrange = 1.5, particlesperframe = 5, particlelife = 75, drawtype = particles.DRAWTYPE_SCALELINE, colour = (255, 255, 255), length = 10.0)
	testsource.CreateParticleKeyframe(50, colour = (3, 74, 236), length = 10.0)
	testsource.CreateParticleKeyframe(75, colour = (255, 255, 0), length = 10.0)
	testsource.CreateParticleKeyframe(100, colour = (0, 255, 255), length = 10.0)
	testsource.CreateParticleKeyframe(125, colour = (0, 0, 0), length = 10.0)

	pygame.mixer.music.load('backgroundMenuMusic.mp3')
	pygame.mixer.music.play(-1)
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

		screen.blit(bg, (0, 0))
		test.Update()
		test.Redraw()
		for option in options:
			if option.rect.collidepoint(pygame.mouse.get_pos()):
				option.hovered = True
			else:
				option.hovered = False
			option.draw()

		if (not isEffect(pygame.mixer.music.get_pos())):
			filter = pygame.surface.Surface((width, height))
			filter.fill(pygame.color.Color('White'))
			filter.blit(light, tuple(map(lambda x: x - 50, pygame.mouse.get_pos())))
			screen.blit(filter, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
			pygame.display.flip()

		pygame.display.update()
