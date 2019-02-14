using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using ESFrontend.Models;

namespace ESFrontend.Controllers
{
    public class HomeController : Controller
    {
        public IActionResult Index(int id)
        {
            if(id == 0) {
                id = 7;
            }
            return View(new SlouchGraphModel(id).Points);
        }

        public IActionResult Notifications() 
        {
            return View(new SlouchGraphModel(2).Points);
        }

        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
